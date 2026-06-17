from mcp.server.fastmcp import FastMCP
from sql_tools import get_top_product, get_total_revenue

mcp = FastMCP("Sales Analytics")


@mcp.tool()
def top_selling_product():
    result = get_top_product()

    product = result.iloc[0]["product_name"]
    quantity = int(result.iloc[0]["total_quantity"])

    return f"{product} sold {quantity} units"


@mcp.tool()
def total_business_revenue():
    result = get_total_revenue()

    revenue = int(result.iloc[0]["revenue"])

    return f"Total business revenue is ₹{revenue}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")