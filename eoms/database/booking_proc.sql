DROP PROCEDURE IF EXISTS process_booking;

DELIMITER $$

CREATE PROCEDURE process_booking(
    IN p_cart_id INT,
    IN p_customer_id INT,
    IN p_store_id INT,
    IN p_note TEXT,
    OUT p_booking_id INT
)
BEGIN
    DECLARE available_count INT;
    DECLARE cart_count INT;

    -- Start the transaction
    START TRANSACTION;

    -- Check if all items in the cart are available
    SELECT COUNT(*) INTO available_count
    FROM (
        SELECT ci.product_code, ci.hire_from, ci.hire_to, ci.qty AS needed_qty, COUNT(m.machine_id) AS available_qty
        FROM cart_item ci
        LEFT JOIN machine m ON ci.product_code = m.product_code
        LEFT JOIN booking_item bi ON m.machine_id = bi.machine_id
            AND bi.hire_from < ci.hire_to AND bi.hire_to > ci.hire_from
        WHERE ci.cart_id = p_cart_id
            AND m.store_id = p_store_id
            AND bi.machine_id IS NULL
        GROUP BY ci.product_code, ci.hire_from, ci.hire_to
        HAVING available_qty >= needed_qty
    ) AS availability_check;

    -- Count the total items in the cart (considering qty)
    SELECT COUNT(*) INTO cart_count
    FROM cart_item
    WHERE cart_id = p_cart_id;

    IF available_count = cart_count THEN
        -- Create a new booking record with a placeholder total
        INSERT INTO booking (customer_id, store_id, create_date, note)
        VALUES (p_customer_id, p_store_id, NOW(), p_note);

        -- Get the last inserted booking ID
        SET p_booking_id = LAST_INSERT_ID();

        -- Initialize the line number
        SET @line_num = 0;
        
        -- Transfer items from cart to booking
        -- For each cart item, insert multiple booking items if qty > 1
        INSERT INTO booking_item (booking_id, machine_id, line_num, hire_rate, hire_from, hire_to)
        SELECT p_booking_id, machine_id, @line_num := @line_num + 1 AS line_num, hire_rate, hire_from, hire_to
        FROM (
            SELECT 
                ci.product_code, 
                m.machine_id, 
                ci.hire_rate * (1 - ci.disc_rate / 100) AS hire_rate,
                ci.hire_from, 
                ci.hire_to, 
                ci.qty,
                ROW_NUMBER() OVER (PARTITION BY ci.product_code ORDER BY ci.hire_from) AS row_num
            FROM 
                cart_item ci
            LEFT JOIN 
                machine m ON ci.product_code = m.product_code
            LEFT JOIN 
                booking_item bi ON m.machine_id = bi.machine_id
                    AND bi.hire_from < ci.hire_to 
                    AND bi.hire_to > ci.hire_from
            WHERE 
                ci.cart_id = p_cart_id
                AND m.store_id = p_store_id
                AND bi.machine_id IS NULL
        ) AS subquery
        WHERE 
            row_num <= qty;

        -- Calculate the booking total based on the days and update the booking
        UPDATE booking
        SET total = (
            SELECT SUM(CEIL(DATEDIFF(bi.hire_to, bi.hire_from)) * bi.hire_rate)
            FROM booking_item bi
            WHERE bi.booking_id = p_booking_id
        )
        WHERE booking_id = p_booking_id;

        -- Insert payment record
        INSERT INTO payment (booking_id, create_date, amount)
        SELECT p_booking_id, NOW(), total
        FROM booking
        WHERE booking_id = p_booking_id;

        -- Insert hire records

        INSERT INTO hire_record (booking_item_id)
        SELECT booking_item_id
        FROM booking_item
        WHERE booking_id = p_booking_id;

        -- Clear the cart_item and remove promo code
        DELETE FROM cart_item WHERE cart_id = p_cart_id;
        UPDATE cart SET promo_code = NULL WHERE cart_id = p_cart_id;

        -- Commit the transaction
        COMMIT;

    ELSE
        -- Rollback the transaction
        ROLLBACK;

        -- Set the booking ID to NULL to indicate failure
        SET p_booking_id = NULL;
    END IF;

END$$

DELIMITER ;
