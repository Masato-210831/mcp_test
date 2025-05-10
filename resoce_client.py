import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_resources():
    server_params = StdioServerParameters(
        command="python",
        args=["resorce.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # リソース一覧を取得

            print("=== Resource List ===")

            resources_result = await session.list_resources()

            for resource in resources_result.resources:
                print(f"- {resource.name}")

            # テストリソースを読む

            print("\n=== Test Resource ===")

            response = await session.read_resource("test://sample")

            print("Response structure:")

            print(f"Type: {type(response)}")

            print(f"Value: {response}")

            if isinstance(response, tuple) and len(response) == 2:
                meta, contents = response

                print(f"\nMeta: {meta}")

                print(f"Contents type: {type(contents)}")

                if isinstance(contents, list):
                    print("\nContents list:")

                    for item in contents:
                        print(f"Item type: {type(item)}")

                        print(f"Item: {item}")

                        if hasattr(item, "text"):
                            print(f"Text: {item.text}")

                        elif isinstance(item, dict) and "text" in item:
                            print(f"Text: {item['text']}")

                        elif isinstance(item, str):
                            print(f"Text: {item}")

            # ファイル一覧を取得

            print("\n=== Files List ===")

            try:
                response = await session.read_resource("files://list")

                print(f"Files response: {response}")

                if isinstance(response, tuple) and len(response) == 2:
                    meta, contents = response

                    if isinstance(contents, list) and contents:
                        content_item = contents[0]

                        if hasattr(content_item, "text"):
                            files_content = content_item.text

                        elif isinstance(content_item, dict) and "text" in content_item:
                            files_content = content_item["text"]

                        elif isinstance(content_item, str):
                            files_content = content_item

                        else:
                            files_content = str(content_item)

                        print("\nFiles in directory:")

                        for file in files_content.split("\n"):
                            print(f"- {file}")

            except Exception as e:
                print(f"Error processing files list: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_resources())
