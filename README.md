# QRtist

QRtist is a simple and user-friendly web application built with **Django** and **Django REST Framework (DRF)** that allows users to generate QR codes from text, PDF, images, and website links. It provides a clean web interface using Django templates and can be used for personal or small-scale projects.

---

## Features

* Generate QR codes from:

  * Text
  * Website URLs
  * PDF files
  * Images
* Download generated QR codes
* Simple and responsive web interface
* Lightweight and easy to deploy

---

## Demo

Example: `https://qrfy.com/`


---

## Tech Stack

* **Backend:** Django, Django REST Framework
* **Frontend:** Django Templates, HTML, CSS, JavaScript
* **QR Code Generation:** [qrcode](https://pypi.org/project/qrcode/) Python library
* **Database:** SQLite (default, can be switched to PostgreSQL for production)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/QRtist.git
cd QRtist
```

2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Run the development server**

```bash
python manage.py runserver
```

6. Open your browser and go to:

```
http://127.0.0.1:8000
```

---

## Usage

1. Go to the home page.
2. Select the type of input (Text, URL, PDF, Image).
3. Enter or upload your input.
4. Click **Generate QR Code**.
5. Download or save your QR code.

---

## API Endpoints (DRF)

For programmatic access, QRtist provides API endpoints:

| Endpoint         | Method | Description                 |
| ---------------- | ------ | --------------------------- |
| `/api/qr/text/`  | POST   | Generate QR from text       |
| `/api/qr/url/`   | POST   | Generate QR from a URL      |
| `/api/qr/pdf/`   | POST   | Generate QR from a PDF file |
| `/api/qr/image/` | POST   | Generate QR from an image   |

*Example request (JSON):*

```json
{
  "text": "Hello, QRtist!"
}
```

---

## Requirements

* Python 3.10+
* Django 6.x
* Django REST Framework
* qrcode
* Pillow (for image handling)

---

## Contributing

1. Fork the repository
2. Create your branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact

**Author:** Maruf Hossain  
Dept. of CSE, Green University of Bangladesh   
Email: [maruf.bshs@gmail.com](mailto:maruf.bshs@gmail.com)    
