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
