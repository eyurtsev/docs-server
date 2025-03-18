from typing import TypedDict, List, NotRequired

import httpx
from markdownify import markdownify
from mcp.server.fastmcp import FastMCP


class DocSource(TypedDict):
    """A source of documentation for a product."""

    name: NotRequired[str]
    llms_txt: str


def create_server(
    doc_source: List[DocSource],
    *,
    follow_redirects: bool = False,
    timeout: float = 10,
) -> FastMCP:
    """Create the server and generate tools."""
    server = FastMCP(name="llms-txt")
    httpx_client = httpx.AsyncClient(follow_redirects=follow_redirects, timeout=timeout)

    @server.tool
    def list_doc_sources() -> str:
        """List all available doc sources. Always start from this tool before fetching any particular content."""
        content = ""
        for entry in doc_source:
            name = entry.get("name", "")
            content += f"{name}\n"
            content += "URL: " + entry["llms_txt"] + "\n\n"
        return content

    # Parse the domain names in the llms.txt URLs
    allowed_domains = []

    @server.tool
    async def fetch_docs(url: str) -> str:
        """Use this to fetch documentation from a given URL."""
        if not any(url.startswith(domain) for domain in allowed_domains):
            return (
                "Error: URL not allowed. Must start with one of the following domains: "
                + ", ".join(allowed_domains)
            )

        try:
            response = await httpx_client.get(url, timeout=timeout)
            response.raise_for_status()
            return markdownify(response.text)
        except httpx.HTTPStatusError as e:
            return "Encountered an HTTP error with code " + str(e.response.status_code)

    return server


#
# async def run_sse(server: FastMCP, transport: ) -> None:
#     """Run the server."""
#     server.run()
#     await server.run()
#
#
# if __name__ == "__main__":
#     server = create_server(
#         [
#             {
#                 "name": "LifterLMS",
#                 "llms_txt": "https://lifterlms.com/llms.txt",
#             },
#             {
#                 "name": "WooCommerce",
#                 "llms_txt": "https://woocommerce.com/llms.txt",
#             },
#         ]
#     )
#     server.run()
