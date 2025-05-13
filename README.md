Got it — your lead engineer is 100% correct. Since your Angular app is part of a Single-SPA microfrontend architecture, your index.html won’t be used directly when the app is mounted. Scripts added there (like the Asprise CDN link) won’t be executed.

⸻

Goal: Dynamically load the Asprise CDN script from your Angular AppComponent (or another root component)

This is the best approach when working with Single-SPA.

⸻

Step-by-Step: Load Asprise Scanner Script in AppComponent
	1.	Remove the <script> tag from index.html, if still present:

<script src="https://asprise.azureedge.net/scannerjs/scanner.js"></script> <!-- REMOVE THIS -->


	2.	In your AppComponent, dynamically load the script:
In app.component.ts:

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
        // Optional: Initialize or test something here
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


	3.	Use the scanner normally in your component once it’s loaded.
After scanner.js is loaded, you can call:

Scanner.scan(displayScanResult, {
  output_settings: [{ type: 'return-base64', format: 'jpg' }]
});

function displayScanResult(successful, mesg, response) {
  // handle scanned image
}



⸻

Bonus: Prevent Multiple Loads

The script.id = 'asprise-scanner' line helps prevent the script from being loaded multiple times, even if the component remounts.

⸻

Alternate: Host Locally

If you’d prefer to download and host the script yourself, you can:
	1.	Download scanner.js from Asprise CDN.
	2.	Place it in src/assets/scanner/ in your Angular app.
	3.	Change the script URL in the code above to:

script.src = '/assets/scanner/scanner.js';



⸻

Let me know which path you want to go with or if you want to auto-trigger the scanner once loaded.
