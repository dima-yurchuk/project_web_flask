from app import create_app

if __name__=='__main__':
    app_run = create_app()
    app_run.run(debug=True)