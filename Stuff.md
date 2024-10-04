Azure Entra ID Authentication and MFA Integration for Swagger UI (Current Project vs. Proposed Implementation)

Based on the current findings and research, this document highlights what is used in the current XYZ Project and proposes how Azure Entra ID authentication and MFA can be implemented in future projects.

1. What the Current XYZ Project Uses in Program.cs

In the current XYZ project, the Program.cs file is configured to use OptumAuth and JWT Bearer Authentication. Swagger UI is set up to use OAuth2 with the following configuration:

app.UseSwaggerUI(options =>
{
    options.OAuthClientId("<xyz-client-id>");
    options.OAuthClientSecret("<xyz-client-secret>");
    options.OAuthScopes("openid", "<custom-api-scope>");
    options.OAuthUsePkce();
    options.OAuthUseBasicAuthenticationWithAccessCodeGrant();
});

2. Proposed Implementation for Azure Entra ID

For future projects, here’s how Azure Entra ID authentication and MFA can be integrated, replacing the current setup with Azure Entra ID using OAuth2 and PKCE for securing APIs and Swagger UI:

Step 1: Azure Entra ID Setup

	•	App Registration: Register the app in Azure AD, enable ID tokens and Access tokens, and configure the Swagger redirect URL.
	•	API Permissions: Add permissions like openid, profile, and custom API scopes in Azure Entra ID.

Step 2: Program.cs Configuration

Replace the current Program.cs setup with the following:

var builder = WebApplication.CreateBuilder(args);

// Add Azure Entra ID Authentication
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(options =>
    {
        options.Instance = "https://login.microsoftonline.com/";
        options.ClientId = "<your-client-id>";
        options.TenantId = "<your-tenant-id>";
        options.CallbackPath = "/signin-oidc";
        options.SaveTokens = true;
    });

// Add Swagger with OAuth2 and PKCE for Azure Entra ID
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();

app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "My API V1");
    options.OAuthClientId("<your-client-id>");
    options.OAuthClientSecret("<your-client-secret>"); // If using confidential client
    options.OAuthUsePkce(); // Use PKCE for secure OAuth2
    options.OAuthScopes("openid", "profile", "<your-api-scope>");
});

app.MapControllers();
app.Run();

Step 3: Enabling MFA in Azure Entra ID

To further secure the API with MFA:

	1.	In Azure AD, go to Security > Conditional Access.
	2.	Create a policy requiring MFA for the app.
	3.	Under Grant, enable Require multi-factor authentication.

Summary: XYZ Project vs. Proposed Implementation

	•	Current Project: The current XYZ project uses OptumAuth and OAuth2 for Swagger UI with Client ID, Client Secret, and PKCE.
	•	Proposed Implementation: The future projects can leverage Azure Entra ID authentication via OAuth2, PKCE, and MFA enforced through Azure Conditional Access.

You can copy and paste the provided configurations and adjust them with relevant ClientId, TenantId, and API Scopes to implement this in other projects!
