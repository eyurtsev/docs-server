# MCP LLMS-TXT Documentation Server

A Model Control Protocol (MCP) server for serving documentation from llms.txt files.

## Installation

```bash
pip install mcp-llms-txt
```

## Usage

### Command-line Interface

The `llms-txt` command provides a simple CLI for launching the documentation server. You can specify documentation sources in three ways:

1. Using a YAML config file:

```bash
llms-txt --yaml sample_config.yaml
```

2. Using a JSON config file:

```bash
llms-txt --json sample_config.json
```

3. Directly specifying llms.txt URLs:

```bash
llms-txt --urls https://lifterlms.com/llms.txt https://woocommerce.com/llms.txt
```

### Additional Options

- `--follow-redirects`: Follow HTTP redirects (defaults to False)
- `--timeout SECONDS`: HTTP request timeout in seconds (defaults to 10.0)

Example with additional options:

```bash
llms-txt --yaml sample_config.yaml --follow-redirects --timeout 15
```

### Configuration Format

Both YAML and JSON configuration files should contain a list of documentation sources. Each source must include an `llms_txt` URL and can optionally include a `name`:

```yaml
- name: LifterLMS
  llms_txt: https://lifterlms.com/llms.txt

- name: WooCommerce
  llms_txt: https://woocommerce.com/llms.txt
```

### Programmatic Usage

```python
from mcp_llms_txt.main import create_server

# Create a server with multiple documentation sources
server = create_server(
    [
        {
            "name": "LifterLMS",
            "llms_txt": "https://lifterlms.com/llms.txt",
        },
        {
            "name": "WooCommerce",
            "llms_txt": "https://woocommerce.com/llms.txt",
        },
    ],
    follow_redirects=True,
    timeout=15.0,
)

# Run the server
server.run(transport="stdio")
```