# FisioVis

_This is a Computer Vision Project developed in django, designed to analize body postures, calculate angles (goniometry) and generate progress reports for physiotherapy patients. This application implements open source models (MediaPipe) and Artificial Intelligence to be the best complement for the professionals in the health area._

_The objective of this app, on addition to being educational, is to provide a secure, fast and accessible solution for the physiotherapy professionals. It's designed for users that prefer to include AI in their workflows, specially for physiotherapy students_

## Starting 🚀

_These instructions will allow you to get a working copy of the project on your local machine for development._


### Prerequisites 📋

_Before you begin, make sure you have the following installed:_

- [Python](https://www.python.org/) ( (recommended version: 3.11 or latest))
- [Git](https://git-scm.com) (It's optional but recommended)
- [PostgreSQL](https://www.postgresql.org/) (Make sure it's installed and running)

### Installation 🔧

1. Clone the repository
```
https://github.com/Loperaa-Juan/FisioVis
```

2. Set Up Virtual Environment

First, create the `venv` folder

```python
# Windows
python -m venv venv

# MacOS or Linux
python3 -m venv venv
```

Activate the virtual environment

```python
# Windows
.\venv\Scripts\activate

# MacOS or Linux
source venv/bin/activate 
```

3. Install Dependencies

Install the required Python packages using `pip`.
```python
pip install -r requirements.txt
```

4. Configure Environment Variables

Create a `.env` file in the root of the project. You can use `.env.example` as a template.

Update the `.env` file with your database credentials and other necessary configurations.