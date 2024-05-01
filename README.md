# cybersecurity-cat-clinic

## Instructions
1. Open the root folder in your temrinal
2. Generate keys with the following command:
   
   ```openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365```
3. ```pip install -r requirements.txt```
4. Run server.py  
5. Open the following URL in your browser:

   ```https://localhost:1642/```
6. Click on advanced at the bottom, and continue anyway
