import React, { useState, useEffect } from "react";

function DynamicMicroserviceComponent() {
  const [microserviceContent, setMicroserviceContent] = useState(null);

  function utf8ToBase64(str) {
    return window.btoa(unescape(encodeURIComponent(str)));
  }

  useEffect(() => {
    async function loadMicroserviceContent() {
      try {
        // Dynamically load the microservice's frontend assets via URL
        const response = await fetch("http://localhost:3000/static/js/index.js");
        const htmlContent = await response.text();
        console.log(htmlContent);

        // Parse the HTML content to extract asset URLs
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = htmlContent;

        const assetUrls = [];
        const assetElements = tempDiv.querySelectorAll(
          "link[href], script[src], img[src]"
        );
        assetElements.forEach((element) => {
          const url =
            element.getAttribute("href") || element.getAttribute("src");
          if (url && !assetUrls.includes(url)) {
            assetUrls.push(url);
          }
        });

        // Fetch each asset individually
        const assetPromises = assetUrls.map(async (url) => {
          const assetResponse = await fetch(url);
          const assetText = await assetResponse.text();
          return utf8ToBase64(assetText);
        });

        // Wait for all asset fetches to complete
        const assets = await Promise.all(assetPromises);

        // Replace asset URLs in the HTML content with fetched asset content
        let updatedHtmlContent = htmlContent;
        assetUrls.forEach((url, index) => {
          updatedHtmlContent = updatedHtmlContent.replace(
            url,
            `data:text/plain;base64,${assets[index]}`
          );
        });

        // Set the microservice content with updated HTML content
        setMicroserviceContent(updatedHtmlContent);
      } catch (error) {
        console.error("Error loading microservice content:", error);
      }
    }

    loadMicroserviceContent();
  }, []);

  return (
    <div>
      {microserviceContent ? (
        // Render the microservice content dynamically
        <div dangerouslySetInnerHTML={{ __html: microserviceContent }} />
      ) : (
        <div>Loading microservice content...</div>
      )}
    </div>
  );
}

export default DynamicMicroserviceComponent;
