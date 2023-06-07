from app.main import app

if __name__ == "__main__":
    app.run(debug=True,port=3010)

    # To Run in production command:
    #1.Choose a production WSGI server: There are several options available, such as Gunicorn, uWSGI, and mod_wsgi. You can choose the one that best suits your needs and preferences. For example, let's use Gunicorn in this explanation.
    #2.Install the WSGI server: If you haven't installed Gunicorn, you can do so using pip, the Python package manager, by running the following command in your terminal:pip install gunicorn
    #3.Start the WSGI server: In your terminal, navigate to the directory containing the wsgi.py file and run the following command:gunicorn wsgi:app







