# Integrating Asprise Scanner.js in Angular (Single-SPA)

In a **Single-SPA microfrontend** architecture, your Angular app is loaded as a Webpack module (`main.js`) and **`index.html` is ignored**. Therefore, scripts added to `index.html` (like Asprise's `scanner.js` CDN link) won't be executed.

This guide helps you load the **Asprise Scanner.js** script dynamically from your Angular app component.

---

## Step 1: Remove CDN Script from `index.html`

If you previously added this to your `index.html`, **remove it**:

```html
<!-- Remove this -->
<script src="https://asprise.azureedge.net/scannerjs/scanner.js"></script>


import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  ngOnInit(): void {
    this.loadScannerScript();
  }

  loadScannerScript(): void {
    const existingScript = document.getElementById('asprise-scanner') as HTMLScriptElement;
    if (!existingScript) {
      const script = document.createElement('script');
      script.src = 'https://asprise.azureedge.net/scannerjs/scanner.js';
      script.id = 'asprise-scanner';
      script.type = 'text/javascript';
      script.onload = () => {
        console.log('Asprise scanner.js loaded.');
        // Optional: initialize scanner logic here
      };
      script.onerror = () => {
        console.error('Failed to load Asprise scanner.js');
      };
      document.body.appendChild(script);
    } else {
      console.log('Asprise scanner.js already loaded.');
    }
  }
}

Scanner.scan(displayScanResult, {
  output_settings: [{ type: 'return-base64', format: 'jpg' }]
});

function displayScanResult(successful: boolean, mesg: string, response: string) {
  // handle scanned image or error
}

// connect-src 'self' https: wss://local.scannerjs.com:9714;



<meta http-equiv="Content-Security-Policy" content="default-src 'self' https: localhost:* https://*.maze.co/; img-src 'self' https: localhost:* data:; script-src 'unsafe-inline' 'unsafe-eval' https: localhost:*; connect-src 'self' https: localhost:* ws://localhost:* wss://* wss://local.scannerjs.com:9714; style-src 'unsafe-inline' https:; object-src 'none'; worker-src blob:;">


Unfortunately, CSP wildcards don’t work the way we’d hope in this case. Specifically:
	•	wss://localhost:* only matches exactly localhost — it does not include local.scannerjs.com
	•	Wildcards like wss://local*:* are not valid in CSP syntax — domain wildcards must be in the form of *.domain.com, and ports must be specific or fully wildcarded (:* isn’t valid)

Because local.scannerjs.com is a loopback alias with a non-standard port (:9714), it needs to be explicitly declared like this:
wss://local.scannerjs.com:9714

So we need to keep wss://* (for general WebSocket use), and add this specific one for Asprise to function properly.
