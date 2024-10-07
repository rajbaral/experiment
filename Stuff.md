
Here’s the final updated documentation that includes the latest information regarding MFA enforcement via Azure Entra ID in conjunction with Swagger UI configured with OAuth2 and PKCE:

Azure Entra ID Authentication and Authorization with MFA Enforcement in Swagger UI for Azure US Government Cloud

Authentication Overview

	•	JWT Bearer Authentication:
	•	Azure Entra ID issues JWT Bearer tokens for secure authentication.
	•	The tokens are validated using the Authority (Azure AD endpoint), Audience (API Client ID), and Issuer (Azure tenant).
	•	The following token parameters are validated:
	•	Issuer: To ensure the token was issued by the correct Azure AD tenant.
	•	Audience: To confirm the token is intended for your API.
	•	Lifetime and Signing Key: To verify the token’s validity and that it has not been tampered with.

Authorization with Custom Policies

	•	Role-Based Access Control (RBAC):
	•	Custom authorization policies are implemented based on roles or claims in the user’s JWT token.
	•	Example policies like "AdminPolicy" and "ViewPolicy" enforce RBAC by validating the roles issued by Azure Entra ID.
	•	Example Custom Policies:
	•	Admin Policy:

options.AddPolicy("AdminPolicy", policy => 
    policy.RequireClaim("roles", "Admin"));


	•	Viewer Policy:

options.AddPolicy("ViewPolicy", policy => 
    policy.RequireClaim("roles", "Viewer"));


	•	Policy Application:
	•	These policies are applied at the controller or action level using the [Authorize] attribute. For example:

[Authorize(Policy = "AdminPolicy")]
public IActionResult AdminAction() 
{
    // Logic for admin users
}



Swagger UI Configuration for Azure Government Cloud

	•	Conditional Swagger UI Setup:
	•	Swagger UI is conditionally enabled for Azure US Government Cloud based on the IsAzureUSGovernment flag in appsettings.json.
	•	OAuth2 with PKCE is used for secure authentication through Azure Entra ID.
	•	OAuth2 Configuration for Swagger UI:
	•	Client ID, Client Secret, and Scopes are dynamically loaded from appsettings.json, making it flexible and adaptable across environments.
	•	OAuth2 Authorization Code Flow with PKCE is used for secure token exchange, ensuring that the OAuth2 flow is secure.
	•	Example Code for Conditional Swagger Setup in Program.cs:

if (builder.Configuration.GetValue<bool>("IsAzureUSGovernment"))
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        var authSection = builder.Configuration.GetSection("Auth");
        options.OAuthClientId(authSection["ClientId"]);
        options.OAuthClientSecret(authSection["ClientSecret"]);
        options.OAuthScopes(JsonSerializer.Deserialize<string[]>(authSection["Scopes"]));
        options.OAuthUsePkce(); // PKCE for secure OAuth2
    });
}



Enforcing MFA with Azure Entra ID

Multi-Factor Authentication (MFA) is enforced via Azure Conditional Access Policies in Azure Entra ID. Swagger UI itself does not handle MFA, but it interacts with Azure Entra ID for authentication.

	•	How MFA is Triggered:
	•	MFA is enforced by Azure Entra ID whenever a user attempts to authenticate via Swagger UI (OAuth2 flow).
	•	If an MFA Conditional Access Policy is configured in Azure Entra ID, the user will be prompted to complete MFA (e.g., through SMS code, authenticator app, etc.) before receiving an access token.
	•	Steps to Set Up MFA in Azure Entra ID:
	1.	Go to Azure Active Directory > Security > Conditional Access.
	2.	Create a Conditional Access Policy targeting the users/groups who should require MFA.
	3.	Under Cloud Apps, select the API application you are securing.
	4.	In the Grant section, enable Require multi-factor authentication.
	5.	Save and enforce the policy.

Once this policy is set up, any user authenticating via Swagger UI will be prompted for MFA if required by the policy.

Environment-Specific Configuration

	1.	appsettings.json for Azure US Government Cloud:

{
  "Auth": {
    "Authority": "https://login.microsoftonline.us/<tenant-id>",
    "Audience": "<api-client-id>",
    "Issuer": "https://login.microsoftonline.us/<tenant-id>/v2.0",
    "ClientId": "<your-client-id>",
    "ClientSecret": "<your-client-secret>",
    "Scopes": "[\"openid\", \"profile\", \"api://<your-api-client-id>/scope\"]"
  },
  "IsAzureUSGovernment": true
}

	•	ClientId and ClientSecret are required for OAuth2 with PKCE in Swagger UI.
	•	Scopes define the permissions requested from Azure Entra ID.

Testing MFA with Swagger UI

	1.	MFA Enforcement in Swagger UI:
	•	When a user clicks “Authorize” in Swagger UI, they are redirected to Azure Entra ID for authentication.
	•	If MFA is enabled via Azure Conditional Access policies, they will be prompted to complete the MFA process before receiving an access token.
	2.	Local Testing:
	•	Ensure IsAzureUSGovernment is set to false for local development without Swagger UI conditional setup.
	3.	Cloud Testing:
	•	Set IsAzureUSGovernment to true for the Azure US Government Cloud deployment to test MFA and OAuth2 with PKCE.

Summary

	1.	Authentication: JWT Bearer tokens are validated using Azure Entra ID for secure API access.
	2.	Authorization: Custom role-based policies (e.g., AdminPolicy, ViewPolicy) are applied based on Azure Entra ID roles.
	3.	Swagger UI: OAuth2 with PKCE is used for secure API testing. The Swagger UI setup is conditional for Azure US Government Cloud.
	4.	MFA Enforcement: MFA is enforced by Azure Entra ID via Conditional Access Policies, requiring users to complete MFA before receiving access tokens in Swagger UI.

This updated document provides a complete guide for your solution with MFA enforcement through Azure Entra ID in Swagger UI, along with the necessary configurations for Azure US Government Cloud.

Let me know if there are any further updates you’d like to add!
