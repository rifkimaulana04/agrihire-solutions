# AgriHire Solutions Equipment and Order Management System

A comprehensive web application for managing agricultural equipment rentals, inventory, bookings and customer relationships. Built with Python Flask and MySQL.

## Features

### Customer Portal
- Equipment browsing and searching with detailed product information 
- Shopping cart functionality with real-time availability checking
- Online booking and payment processing
- Account management and booking history
- Promotional code support
- Store locator with distance calculation
- Customer messaging system

### Staff Portal
- Equipment check-in/check-out management
- Real-time inventory tracking
- Equipment maintenance records
- Customer booking management
- Store-specific reporting

### Management Portal
- Multi-store inventory management
- Staff and customer management
- Promotional campaign management 
- Financial reporting
- Equipment utilization analytics
- Store performance monitoring

### System Features
- Role-based access control (Customer, Staff, Local Manager, National Manager, Admin)
- Real-time availability checking
- Automated notifications
- Equipment maintenance tracking
- Multi-store support
- Responsive design

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Flask-WTF with BCrypt
- **Form Handling**: WTForms
- **Address Validation**: Addy API
- **Visualization**: ECharts
- **Additional Libraries**: 
  - geopy (distance calculations)
  - mysql-connector-python
  - requests
  - email_validator

## Getting Started

### Prerequisites
- Python 3.x
- MySQL
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/ChanMeng666/AgriHire-Solutions.git
```

2. Create and configure database connection
Create `connect.py` under `eoms` folder with your database configuration:
```python
dbuser = "your_username"
dbpass = "your_password" 
dbhost = "localhost"
dbport = "3306"
dbname = "agrihire"
```

3. (Optional) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Create database
- Run `database/agrihire_db+data.sql` to create database schema and sample data
- Disable Safe Updates mode in MySQL Workbench if needed

6. Start the application
```bash
python run.py
```

## Role-Based Access Control

### Access Permissions Matrix

| Function                   | Admin/National Manager | Local Manager/Staff      | Customer        |
| -------------------------- | ---------------------- | ------------------------ | --------------- |
| View Financial Reports     | Access all data        | Store-specific data only | No access       |
| View Hire Status           | Access all data        | Store-specific data only | No access       |
| View Maintenance Records   | Access all data        | Store-specific data only | No access       |
| Stock/Order/Store Reports  | Full access            | View only                | No access       |
| View Product Inventory     | Access all data        | Store-specific data only | View only       |
| View Customer Orders       | Access all data        | Store-specific data only | Own orders only |
| View Store Distribution    | Full access            | No access                | View only       |
| User Roles Distribution    | Full access            | No access                | No access       |
| User Activity Distribution | Full access            | No access                | No access       |
| Equipment Management       | Full access            | Store-specific only      | No access       |
| Staff Management           | Full access            | Store-specific only      | No access       |
| Customer Management        | Full access            | View only                | No access       |
| Promotion Management       | Full access            | Store-specific only      | No access       |

### Test Accounts

All accounts use the same password: `Test1234!`

#### Customer Accounts

| Email           | Role     |
| --------------- | -------- |
| cust1@email.com | customer |
| cust2@email.com | customer |
| cust3@email.com | customer |
| cust4@email.com | customer |
| cust5@email.com | customer |

#### Staff Accounts

| Email              | Role  |
| ------------------ | ----- |
| staff1@agrihire.nz | staff |
| staff2@agrihire.nz | staff |
| staff3@agrihire.nz | staff |
| staff4@agrihire.nz | staff |
| staff5@agrihire.nz | staff |
| staff6@agrihire.nz | staff |

#### Management Accounts

| Email                 | Role             |
| --------------------- | ---------------- |
| lmanager1@agrihire.nz | local manager    |
| lmanager2@agrihire.nz | local manager    |
| lmanager3@agrihire.nz | local manager    |
| nmanager1@agrihire.nz | national manager |
| admin1@agrihire.nz    | system admin     |

## System Architecture

### Core Modules

- User Authentication & Authorization
- Equipment Management
- Booking System
- Store Management 
- Customer Relationship Management
- Reporting & Analytics
- Notification System
- Promotional System

### Database Structure

Key tables include:

- user
- customer
- staff
- store
- machine
- product
- booking
- booking_item
- cart
- cart_item
- promotion
- service
- message

## Detailed Features

### Equipment Management

- Complete equipment lifecycle tracking
- Maintenance scheduling and history
- Real-time availability tracking
- Multi-store inventory management
- Equipment categorization and specification management

### Booking System

- Real-time availability checking
- Flexible rental period management
- Automatic price calculation
- Multi-item bookings
- Extension and cancellation handling
- Payment processing integration

### Customer Features

- Self-service booking
- Account management
- Booking history
- Equipment recommendations
- Store locator with distance calculation
- Direct messaging with store staff

### Staff Features

- Equipment check-in/check-out
- Customer management
- Booking management
- Maintenance recording
- Inventory management
- Store-specific reporting

### Management Features

- Multi-store oversight
- Staff management
- Performance analytics
- Financial reporting
- Promotion management
- System configuration

### Promotional System

- Flexible discount rules
- Time-based promotions
- Product-specific promotions
- Store-specific promotions
- Promotional code management

## Development

### Project Structure

```
agrihire/
├── eoms/
│   ├── model/         # Database models
│   ├── route/         # Route handlers
│   ├── form/          # Form definitions
│   ├── static/        # Static assets
│   └── templates/     # HTML templates
├── database/          # SQL scripts
└── requirements.txt   # Dependencies
```

### Development Environment Setup

1. Install MySQL Server and MySQL Workbench
2. Configure MySQL Server:
   - Disable safe updates mode
   - Enable stored procedures
   - Configure for larger result sets
3. Set up Python development environment
4. Configure IDE (recommended: VS Code)

[Rest of the previous sections remain the same...]

## API Documentation

### Core APIs

- Authentication API
- Equipment Management API
- Booking Management API
- Store Management API
- Customer Management API
- Reporting API

Detailed API documentation is available in the project wiki.

## Deployment

### Requirements

- Python 3.8+
- MySQL 8.0+
- Modern web browser with JavaScript enabled
- Minimum 4GB RAM
- 10GB storage space

### Production Considerations

- Configure proper security measures
- Set up backup systems
- Implement monitoring
- Configure email system
- Set up SSL certificates

## Support

For support and questions, please:

1. Check the documentation
2. Raise an issue in the repository
3. Contact the development team

## Contributing

1. Create a new branch
```bash
git checkout -b feature/AmazingFeature
```

2. Commit your changes
```bash 
git commit -m 'Add some AmazingFeature'
```

3. Push to the branch
```bash
git push origin feature/AmazingFeature
```

4. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [ChanMeng666/AgriHire-Solutions](https://github.com/ChanMeng666/AgriHire-Solutions)

Live Demo: [Home](https://agrihireaq.pythonanywhere.com/)
