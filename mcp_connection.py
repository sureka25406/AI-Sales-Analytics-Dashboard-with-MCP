import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def ask_mcp(question):

    async with streamablehttp_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read, write, _):

        async with ClientSession(read, write) as session:

            await session.initialize()

            question = question.lower()


            # Top Selling Product
            if any(word in question for word in [
                "product",
                "highest",
                "top",
                "best",
                "selling",
                "sold"
            ]):

                result = await session.call_tool(
                    "top_selling_product",
                    {}
                )

                return result.content[0].text


            # Total Revenue
            elif any(word in question for word in [
                "revenue",
                "sales",
                "income",
                "money"
            ]):

                result = await session.call_tool(
                    "total_business_revenue",
                    {}
                )

                return result.content[0].text


            else:

                return "Sorry, I can answer only sales related questions."


def get_ai_answer(question):

    return asyncio.run(
        ask_mcp(question)
    )