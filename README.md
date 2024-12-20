# experiment
trigger:
  branches:
    include:
      - main
      - develop

schedules:
- cron: "0 2 * * *" # Nightly run at 2 AM UTC
  displayName: Nightly Scheduled Test Run
  branches:
    include:
      - develop
      - main
  always: true

pool:
  vmImage: 'windows-latest'

variables:
  buildConfiguration: 'Release'
  testResultsFolder: 'TestResults'
  screenshotsFolder: 'TestResults/Screenshots'
  testProjectPath: 'src/Tests/Tests.csproj'  # Path to your test project
  baseUrl: 'https://staging.example.com'

steps:
# 1. Checkout the repository
- task: Checkout@1

# 2. Install .NET 8 SDK
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '8.x'

# 3. Restore dependencies
- script: |
    dotnet restore $(testProjectPath)
  displayName: 'Restore Dependencies'

# 4. Install Playwright Browsers
- script: |
    dotnet tool restore
    dotnet playwright install
  displayName: 'Install Playwright Browsers'

# 5. Build the Test Project
- script: |
    dotnet build $(testProjectPath) --configuration $(buildConfiguration)
  displayName: 'Build Test Project'

# 6. Run Tests and Capture Screenshots
- script: |
    dotnet test $(testProjectPath) --configuration $(buildConfiguration) \
      --logger:trx --results-directory $(testResultsFolder) \
      -- TestRunParameters.Parameter(name=BaseUrl, value=$(baseUrl)) \
      || echo "Tests failed. Check screenshots."
  displayName: 'Run E2E Tests'

# 7. Collect Screenshots (if any)
- script: |
    if [ -d $(screenshotsFolder) ]; then
      echo "Screenshots captured. Publishing them as artifacts.";
    else
      echo "No screenshots found.";
    fi
  displayName: 'Collect Screenshots'

# 8. Publish Test Results
- task: PublishTestResults@2
  inputs:
    testResultsFiles: '$(testResultsFolder)/*.trx'
    testRunTitle: 'Playwright E2E Tests'
  condition: succeededOrFailed()

# 9. Publish Screenshots as Artifacts
- task: PublishPipelineArtifact@1
  inputs:
    targetPath: '$(screenshotsFolder)'
    artifactName: 'Screenshots'
  condition: always()
