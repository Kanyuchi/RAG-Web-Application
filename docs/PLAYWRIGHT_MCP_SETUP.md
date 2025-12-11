# Playwright MCP Server Configuration

## Overview

This project uses the official Microsoft Playwright MCP (Model Context Protocol) server to enable browser automation and testing capabilities during development. The Playwright MCP server allows Claude Code to interact with web browsers, automate testing, take screenshots, and perform web scraping.

## What is Playwright MCP?

Playwright MCP is a Model Context Protocol server that provides browser automation capabilities using Playwright. It enables LLMs (like Claude) to:

- Navigate and interact with web pages
- Take screenshots and generate PDFs
- Execute JavaScript in browser contexts
- Automate testing workflows
- Perform web scraping
- Generate test code automatically

**Key Advantage**: Uses Playwright's accessibility tree rather than pixel-based input, meaning no vision models are needed.

## Installation & Configuration

### Prerequisites

- Node.js 18 or newer (✓ You have v22.14.0 installed)
- npm or npx available

### Configuration File

The Playwright MCP server is configured in `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {}
    }
  }
}
```

This configuration:
- Uses `npx` to run the latest version of `@playwright/mcp`
- Automatically downloads/updates the package when needed
- No additional environment variables required by default

### Advanced Configuration Options

You can customize the Playwright MCP server with additional arguments:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser", "chromium",
        "--headless", "false",
        "--device", "iPhone 13"
      ],
      "env": {
        "PLAYWRIGHT_BROWSERS_PATH": "./browsers"
      }
    }
  }
}
```

**Available Options:**
- `--browser`: Choose browser (chromium, firefox, webkit)
- `--headless`: Run headless (true/false)
- `--device`: Emulate specific device
- `--proxy`: Configure proxy settings
- `--persistent-profile`: Use persistent browser profile
- `--isolated-context`: Use isolated testing context

## Usage Examples

### Testing Your RAG Application

Once the Playwright MCP is configured, you can ask Claude Code to:

1. **Launch and test the FastAPI application:**
   ```
   "Start the FastAPI server and use Playwright to test the /docs endpoint"
   ```

2. **Automate UI testing:**
   ```
   "Navigate to the project creation page and test the file upload functionality"
   ```

3. **Take screenshots:**
   ```
   "Take a screenshot of the main dashboard page"
   ```

4. **Generate test code:**
   ```
   "Create Playwright test scripts for the document upload workflow"
   ```

5. **Web scraping for testing:**
   ```
   "Scrape the API documentation page and verify all endpoints are listed"
   ```

### Integration with RAG Application Development

During development of your RAG application, Playwright MCP can:

- **Test PDF upload functionality** - Automate uploading test PDFs and verify processing
- **Test Google Drive integration** - Simulate OAuth flow and file attachment
- **Verify query responses** - Test the chat interface with various queries
- **Screenshot generation** - Capture UI states for documentation
- **End-to-end testing** - Automate complete user workflows

## Verifying Installation

To verify Playwright MCP is working:

1. Restart Claude Code (if it was running)
2. The MCP server will automatically start when needed
3. Ask Claude: "List available MCP tools" to see Playwright capabilities

## Available Playwright Tools

The Playwright MCP server provides these tools:

- **Navigation**: `goto`, `goBack`, `goForward`, `reload`
- **Interaction**: `click`, `fill`, `select`, `check`, `uncheck`
- **Content**: `getText`, `getHTML`, `evaluate`
- **Screenshots**: `screenshot`, `pdf`
- **Tab Management**: `newTab`, `closeTab`, `switchTab`
- **Assertions**: `waitForSelector`, `waitForNavigation`

## Troubleshooting

### Server Won't Start

1. Check Node.js version: `node --version` (must be 18+)
2. Verify `.mcp.json` syntax is valid JSON
3. Try manual installation: `npx @playwright/mcp@latest --help`

### Browser Installation Issues

If Playwright browsers aren't installed:
```bash
npx playwright install chromium
```

### Permission Errors

On Windows, you may need to run terminal as Administrator for first-time setup.

## Best Practices

1. **Use headless mode in CI/CD**: Set `--headless true` for automated testing
2. **Device emulation**: Test responsive design with `--device` option
3. **Persistent profiles**: Use `--persistent-profile` to maintain login states
4. **Isolated contexts**: Use `--isolated-context` for clean test environments

## Resources

- [Official Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Playwright Documentation](https://playwright.dev/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## Integration with This Project

For this RAG application, Playwright MCP will be particularly useful for:

1. **Frontend Development**: Once you build the React/Next.js frontend
2. **API Testing**: Automated testing of FastAPI endpoints via Swagger UI
3. **PDF Upload Testing**: Simulate real user file upload workflows
4. **Query Interface Testing**: Test the chat/query interface
5. **Documentation**: Screenshot generation for README and docs

---

*Last Updated: 2025-11-04*
