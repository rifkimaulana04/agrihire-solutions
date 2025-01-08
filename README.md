<div align="center">
 <h1>AgriHire Solutions: Equipment and Order Management System</h1>
 <img src="https://img.shields.io/badge/Status-Active-brightgreen"/>
 <img src="https://img.shields.io/badge/License-MIT-blue"/>
 <img src="https://img.shields.io/badge/Version-1.0.0-orange"/>
 <img src="https://img.shields.io/badge/Python-3.8+-green"/>
 <img src="https://img.shields.io/badge/Flask-3.0.2-red"/>
</div>

A comprehensive web application for managing agricultural equipment rentals, inventory, bookings and customer relationships. Built with Python Flask and MySQL.

<br/>

[![Explore GitHub Profile README Generator](https://gradient-svg-generator.vercel.app/?text=👉+Try+It+Now!+👈&height=40&template=pride-rainbow)](https://agrihireaq.pythonanywhere.com/)

<br/>


https://github.com/user-attachments/assets/164c93f0-ef2b-458c-b58c-edfc98c62cac


![screencapture-agrihireaq-pythonanywhere-2024-12-07-19_36_51](https://github.com/user-attachments/assets/49dc71c5-f128-4d59-8bd4-c5bcfffbbff3)

![屏幕截图 2024-12-07 194310](https://github.com/user-attachments/assets/ec1d7670-01fb-4d29-9aee-afe0d097c06d)

![screencapture-agrihireaq-pythonanywhere-for-hire-CHAIN-CHAIN-40PTR-2024-12-09-02_00_11](https://github.com/user-attachments/assets/a69d4bfa-a6f3-4efe-87af-3bf7ee85f984)

![screencapture-agrihireaq-pythonanywhere-cart-2024-12-09-02_00_27](https://github.com/user-attachments/assets/8ab6cc02-5fe2-4ce9-a1e7-28f1e793bb96)

![screencapture-agrihireaq-pythonanywhere-review-booking-2024-12-09-02_01_19](https://github.com/user-attachments/assets/53e92a24-a9ed-4ebe-8d80-86842f6a8854)

![screencapture-agrihireaq-pythonanywhere-machines-2024-12-07-19_38_55](https://github.com/user-attachments/assets/f8c6ba10-fe21-444c-af2a-b2313b965f0f)

![screencapture-agrihireaq-pythonanywhere-stock-order-store-reports-2024-12-07-19_41_19](https://github.com/user-attachments/assets/aa540e8e-c3bb-4382-a2e9-74fd6c8ab570)

![screencapture-agrihireaq-pythonanywhere-calendar-2024-12-07-19_40_47](https://github.com/user-attachments/assets/8400d025-2e84-4161-866c-4e73d88bdf82)

![screencapture-agrihireaq-pythonanywhere-promotion-2024-12-07-19_43_19](https://github.com/user-attachments/assets/eb4346cd-9b0a-4fac-b0f2-541750ea62a2)

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
git clone https://github.com/ChanMeng666/agrihire-solutions.git
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

## Test Accounts

All accounts use the same password: `Test1234!`

### Customer Accounts
| Email           | Role     |
| --------------- | -------- |
| cust1@email.com | customer |
| cust2@email.com | customer |

### Staff Accounts
| Email                 | Role          |
| --------------------- | ------------- |
| staff1@agrihire.nz    | staff         |
| lmanager1@agrihire.nz | local manager |
| admin@agrihire.nz     | admin         |

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

## Contributing

1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## License

Distributed under the [Apache-2.0 license](LICENSE).

## Contact

Project Link: https://agrihireaq.pythonanywhere.com/

## 🙋‍♀ Author

Created and maintained by [Chan Meng](https://github.com/ChanMeng666).
