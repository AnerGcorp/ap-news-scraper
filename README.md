To run this Python application, follow these steps:

1. Create a virtual environment by executing the following command in your terminal:
    ```
    python3 -m venv env
    ```

2. Activate the virtual environment:
    - For Linux/Mac:
      ```
      source env/bin/activate
      ```
    - For Windows:
      ```
      env\Scripts\activate
      ```

3. Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```

4. Ensure that you have the necessary Selenium drivers installed on your computer. If not, download and install the appropriate drivers for your browser.
It is tested on `Ubuntu 24.04`, Chrome driver version: `127.0.6533.72` and Google Chrome browser version: `Version 127.0.6533.72 (Official Build) (64-bit)` 

5. Once the virtual environment is activated and the dependencies are installed, you can start the application by running the following command:
    ```
    python main.py
    ```

Please note that this application has been tested on Ubuntu 24.04. If you encounter any issues, ensure that your environment matches the specified requirements.
