## Configuration
 
In both dev and prod, the system will get configuration options from a `.env` file. Edit your current `.env` file to include these following values. 
 
* `BASE_URL`: The base URL of your application. This must match one of the redirect URIs configured in the Google Cloud Console.
  * `http://localhost:80` in dev
  * `https://<your-subdomain>.moraviancs.click` in prod
* `GOOGLE_CLIENT_ID`: The OAuth 2.0 Client ID from Google Cloud Console
* `GOOGLE_CLIENT_SECRET`: The OAuth 2.0 Client Secret from Google Cloud Console

Before running ./dev_up.sh, add to the .env file in the project root:

```
BASE_URL=http://localhost
GOOGLE_CLIENT_ID=<Get from 1Password under Google Cloud Console>
GOOGLE_CLIENT_SECRET=<get from 1Password under Google Cloud Console>
```

Now install dependencies:
```
pip install -r requirements.txt
```

Run this command if rollout issues persist: 
```
npm install react-router-dom
```
