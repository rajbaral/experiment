
[Binding]
public class Hooks
{
    private readonly IPage _page;  // Inject the Playwright page object
    private readonly ScenarioContext _scenarioContext;

    public Hooks(IPage page, ScenarioContext scenarioContext)
    {
        _page = page;
        _scenarioContext = scenarioContext;
    }

    [AfterScenario]
    public async Task TakeScreenshotOnFailure()
    {
        if (_scenarioContext.TestError != null)  // Capture screenshot if test failed
        {
            var screenshotPath = Path.Combine(Directory.GetCurrentDirectory(), "TestArtifacts", "Screenshots", $"{_scenarioContext.ScenarioInfo.Title}_{DateTime.Now:yyyyMMddHHmmss}.png");
            Directory.CreateDirectory(Path.GetDirectoryName(screenshotPath));
            await _page.ScreenshotAsync(new PageScreenshotOptions { Path = screenshotPath });
            Console.WriteLine($"Screenshot captured: {screenshotPath}");
        }
    }
}




steps:
- task: PublishBuildArtifacts@1
  inputs:
    pathtoPublish: '$(Build.SourcesDirectory)/TestArtifacts/Screenshots'
    artifactName: 'screenshots'
    publishLocation: 'Container'
