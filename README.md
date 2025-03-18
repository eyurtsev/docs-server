# MCP LLMS.txt Tools

A Python package that creates MCP tools for fetching and working with `llms.txt` files.

## Installation

```bash
pip install mcp-llms-txt
```

## Usage

This package provides tools for dynamically generating MCP tools to fetch and work with `llms.txt` files from different products.

### Basic Usage

```python
from mcp.runtime import Runtime
from mcp_llms_txt.tools import server

# Create the runtime
runtime = Runtime()
runtime.add_server(server)

# Option 1: Load from a JSON file
response = await runtime.ainvoke("load_llms_txt_entries_from_json", {
    "json_path": "path/to/entries.json"
})
print(response)

# Option 2: Load from a JSON string
entries_json = '''[
    {
        "product": "Bika.ai",
        "website": "https://bika.ai/",
        "llms-txt": "https://bika.ai/llms.txt",
        "llms-txt-tokens": 541
    },
    {
        "product": "Azumuta",
        "website": "https://www.azumuta.com/",
        "llms-txt": "https://www.azumuta.com/llms.txt",
        "llms-txt-tokens": ""
    }
]'''
response = await runtime.ainvoke("load_llms_txt_entries_from_list", {
    "entries_json": entries_json
})
print(response)

# After loading, you can access the dynamically generated tools
bika_response = await runtime.ainvoke("get_bika_ai_llms_txt", {})
print(bika_response)
```

### Data Format

The tool expects entries in the following JSON format:

```json
[
    {
        "product": "Product Name",       // Name of the product/company
        "website": "https://product.website/",  // Website URL
        "llms-txt": "https://product.website/llms.txt",  // URL to llms.txt file
        "llms-txt-tokens": 123,          // Number of tokens (optional)
        "llms-full-txt": "",             // Full text content (optional)
        "llms-full-txt-tokens": null     // Full text tokens (optional)
    }
]
```

### Generated Tools

For each entry in the list, the tool creates a new MCP tool with a name like `get_<product>_llms_txt` (spaces and special characters converted to underscores). For example, an entry for "Bika.ai" will create a tool named `get_bika_ai_llms_txt`.

These dynamically generated tools fetch the content of the corresponding llms.txt file when invoked.

## License

MIT