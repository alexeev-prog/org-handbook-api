import asyncio
import json
from typing import Any

import aiohttp
import click


class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"X-API-Key": self.api_key}

    async def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        async with (
            aiohttp.ClientSession() as session,
            session.request(method, url, headers=self.headers, **kwargs) as response,
        ):
            response.raise_for_status()
            return await response.json()

    async def get_organizations(self, skip: int = 0, limit: int = 100):
        return await self._request(
            "GET", f"/api/v1/organizations/?skip={skip}&limit={limit}"
        )

    async def get_organization(self, organization_id: int):
        return await self._request("GET", f"/api/v1/organizations/{organization_id}")

    async def create_organization(self, data: dict[str, Any]):
        return await self._request("POST", "/api/v1/organizations/", json=data)

    async def update_organization(self, organization_id: int, data: dict[str, Any]):
        return await self._request(
            "PUT", f"/api/v1/organizations/{organization_id}", json=data
        )

    async def delete_organization(self, organization_id: int):
        return await self._request("DELETE", f"/api/v1/organizations/{organization_id}")

    async def get_organizations_by_building(self, building_id: int):
        return await self._request(
            "GET", f"/api/v1/organizations/building/{building_id}"
        )

    async def get_organizations_by_activity(self, activity_id: int):
        return await self._request(
            "GET", f"/api/v1/organizations/activity/{activity_id}"
        )

    async def search_organizations_by_name(self, name: str):
        return await self._request(
            "GET", f"/api/v1/organizations/search/name?name={name}"
        )

    async def get_organizations_in_radius(
        self, lat: float, lon: float, radius_km: float
    ):
        return await self._request(
            "GET",
            f"/api/v1/organizations/search/radius?lat={lat}&lon={lon}&radius_km={radius_km}",
        )

    async def get_organizations_in_area(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ):
        return await self._request(
            "GET",
            f"/api/v1/organizations/search/area?min_lat={min_lat}&max_lat={max_lat}&min_lon={min_lon}&max_lon={max_lon}",
        )

    async def get_buildings(self, skip: int = 0, limit: int = 100):
        return await self._request(
            "GET", f"/api/v1/building/?skip={skip}&limit={limit}"
        )

    async def get_building(self, building_id: int):
        return await self._request("GET", f"/api/v1/building/{building_id}")

    async def create_building(self, data: dict[str, Any]):
        return await self._request("POST", "/api/v1/building/", json=data)

    async def update_building(self, building_id: int, data: dict[str, Any]):
        return await self._request("PUT", f"/api/v1/building/{building_id}", json=data)

    async def delete_building(self, building_id: int):
        return await self._request("DELETE", f"/api/v1/building/{building_id}")

    async def get_activities(self, skip: int = 0, limit: int = 100):
        return await self._request(
            "GET", f"/api/v1/activity/?skip={skip}&limit={limit}"
        )

    async def get_activity(self, activity_id: int):
        return await self._request("GET", f"/api/v1/activity/{activity_id}")

    async def create_activity(self, data: dict[str, Any]):
        return await self._request("POST", "/api/v1/activity/", json=data)

    async def update_activity(self, activity_id: int, data: dict[str, Any]):
        return await self._request("PUT", f"/api/v1/activity/{activity_id}", json=data)

    async def delete_activity(self, activity_id: int):
        return await self._request("DELETE", f"/api/v1/activity/{activity_id}")

    async def get_activity_tree(self, parent_id: int | None = None):
        endpoint = (
            f"/api/v1/activity/tree/{parent_id}"
            if parent_id
            else "/api/v1/activity/tree/"
        )
        return await self._request("GET", endpoint)

    async def health_check(self):
        return await self._request("GET", "/health")


def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


async def run_async(coro):
    return await coro


@click.group()
@click.option("--base-url", default="http://localhost:8000", help="Base API URL")
@click.option("--api-key", default="secret-static-api-key", help="API Key")
@click.pass_context
def cli(ctx, base_url, api_key):
    ctx.ensure_object(dict)
    ctx.obj["client"] = APIClient(base_url, api_key)


@cli.command()
@click.pass_context
def seed(ctx):
    client = ctx.obj["client"]

    async def seed_data():
        buildings_data = [
            {
                "address": "г. Москва, ул. Ленина 1, офис 3",
                "longitude": 37.6173,
                "latitude": 55.7558,
            },
            {
                "address": "г. Москва, ул. Тверская 10",
                "longitude": 37.6095,
                "latitude": 55.7601,
            },
            {
                "address": "г. Санкт-Петербург, Невский пр. 100",
                "longitude": 30.3351,
                "latitude": 59.9343,
            },
        ]

        activities_data = [
            {"name": "Еда", "parent_id": None, "level": 0},
            {"name": "Мясная продукция", "parent_id": 1, "level": 1},
            {"name": "Молочная продукция", "parent_id": 1, "level": 1},
            {"name": "Автомобили", "parent_id": None, "level": 0},
            {"name": "Грузовые", "parent_id": 4, "level": 1},
            {"name": "Легковые", "parent_id": 4, "level": 1},
            {"name": "Запчасти", "parent_id": 4, "level": 1},
            {"name": "Аксессуары", "parent_id": 7, "level": 2},
        ]

        organizations_data = [
            {
                "legal_name": 'ООО "Рога и Копыта"',
                "building_id": 1,
                "phone_numbers": ["2-222-222", "3-333-333", "8-923-666-13-13"],
                "activity_ids": [2, 3],
            },
            {
                "legal_name": 'ООО "АвтоМир"',
                "building_id": 2,
                "phone_numbers": ["4-444-444", "5-555-555"],
                "activity_ids": [5, 6],
            },
            {
                "legal_name": 'ООО "Запчасти и аксессуары"',
                "building_id": 3,
                "phone_numbers": ["6-666-666"],
                "activity_ids": [8],
            },
        ]

        buildings = []
        for building_data in buildings_data:
            building = await client.create_building(building_data)
            buildings.append(building)
            print(f"Created building: {building['id']}")

        activities = []
        for activity_data in activities_data:
            activity = await client.create_activity(activity_data)
            activities.append(activity)
            print(f"Created activity: {activity['id']} - {activity['name']}")

        for org_data in organizations_data:
            organization = await client.create_organization(org_data)
            print(
                f"Created organization: {organization['id']} - {organization['legal_name']}"
            )

        print("Seed data created successfully!")

    asyncio.run(seed_data())


@cli.group()
@click.pass_context
def organizations(ctx):
    pass


@organizations.command(name="list")
@click.option("--skip", default=0, help="Skip records")
@click.option("--limit", default=100, help="Limit records")
@click.pass_context
def organizations_list(ctx, skip, limit):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_organizations(skip, limit))
    print_json(result)


@organizations.command(name="get")
@click.argument("organization_id", type=int)
@click.pass_context
def organizations_get(ctx, organization_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_organization(organization_id))
    print_json(result)


@organizations.command(name="create")
@click.pass_context
def organizations_create(ctx):
    client = ctx.obj["client"]

    legal_name = click.prompt("Legal Name")
    building_id = click.prompt("Building ID", type=int)

    phone_numbers = []
    while True:
        phone = click.prompt(
            "Phone Number (leave empty to finish)", default="", show_default=False
        )
        if not phone:
            break
        phone_numbers.append(phone)

    activity_ids = []
    while True:
        activity_id = click.prompt(
            "Activity ID (leave empty to finish)", default="", show_default=False
        )
        if not activity_id:
            break
        activity_ids.append(int(activity_id))

    data = {
        "legal_name": legal_name,
        "building_id": building_id,
        "phone_numbers": phone_numbers,
        "activity_ids": activity_ids,
    }

    result = asyncio.run(client.create_organization(data))
    print_json(result)


@organizations.command(name="update")
@click.argument("organization_id", type=int)
@click.pass_context
def organizations_update(ctx, organization_id):
    client = ctx.obj["client"]

    legal_name = click.prompt("Legal Name", default="", show_default=False)
    building_id = click.prompt("Building ID", default="", show_default=False)

    data = {}
    if legal_name:
        data["legal_name"] = legal_name
    if building_id:
        data["building_id"] = int(building_id)

    result = asyncio.run(client.update_organization(organization_id, data))
    print_json(result)


@organizations.command(name="delete")
@click.argument("organization_id", type=int)
@click.pass_context
def organizations_delete(ctx, organization_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.delete_organization(organization_id))
    print_json(result)


@organizations.command(name="by-building")
@click.argument("building_id", type=int)
@click.pass_context
def organizations_by_building(ctx, building_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_organizations_by_building(building_id))
    print_json(result)


@organizations.command(name="by-activity")
@click.argument("activity_id", type=int)
@click.pass_context
def organizations_by_activity(ctx, activity_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_organizations_by_activity(activity_id))
    print_json(result)


@organizations.command(name="search-name")
@click.argument("name")
@click.pass_context
def organizations_search_name(ctx, name):
    client = ctx.obj["client"]
    result = asyncio.run(client.search_organizations_by_name(name))
    print_json(result)


@organizations.command(name="search-radius")
@click.pass_context
def organizations_search_radius(ctx):
    client = ctx.obj["client"]

    lat = click.prompt("Latitude", type=float)
    lon = click.prompt("Longitude", type=float)
    radius_km = click.prompt("Radius (km)", type=float)

    result = asyncio.run(client.get_organizations_in_radius(lat, lon, radius_km))
    print_json(result)


@organizations.command(name="search-area")
@click.pass_context
def organizations_search_area(ctx):
    client = ctx.obj["client"]

    min_lat = click.prompt("Min Latitude", type=float)
    max_lat = click.prompt("Max Latitude", type=float)
    min_lon = click.prompt("Min Longitude", type=float)
    max_lon = click.prompt("Max Longitude", type=float)

    result = asyncio.run(
        client.get_organizations_in_area(min_lat, max_lat, min_lon, max_lon)
    )
    print_json(result)


@cli.group()
@click.pass_context
def buildings(ctx):
    pass


@buildings.command(name="list")
@click.option("--skip", default=0, help="Skip records")
@click.option("--limit", default=100, help="Limit records")
@click.pass_context
def buildings_list(ctx, skip, limit):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_buildings(skip, limit))
    print_json(result)


@buildings.command(name="get")
@click.argument("building_id", type=int)
@click.pass_context
def buildings_get(ctx, building_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_building(building_id))
    print_json(result)


@buildings.command(name="create")
@click.pass_context
def buildings_create(ctx):
    client = ctx.obj["client"]

    address = click.prompt("Address")
    longitude = click.prompt("Longitude", type=float)
    latitude = click.prompt("Latitude", type=float)

    data = {"address": address, "longitude": longitude, "latitude": latitude}

    result = asyncio.run(client.create_building(data))
    print_json(result)


@buildings.command(name="update")
@click.argument("building_id", type=int)
@click.pass_context
def buildings_update(ctx, building_id):
    client = ctx.obj["client"]

    address = click.prompt("Address", default="", show_default=False)
    longitude = click.prompt("Longitude", default="", show_default=False)
    latitude = click.prompt("Latitude", default="", show_default=False)

    data = {}
    if address:
        data["address"] = address
    if longitude:
        data["longitude"] = float(longitude)
    if latitude:
        data["latitude"] = float(latitude)

    result = asyncio.run(client.update_building(building_id, data))
    print_json(result)


@buildings.command(name="delete")
@click.argument("building_id", type=int)
@click.pass_context
def buildings_delete(ctx, building_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.delete_building(building_id))
    print_json(result)


@cli.group()
@click.pass_context
def activities(ctx):
    pass


@activities.command(name="list")
@click.option("--skip", default=0, help="Skip records")
@click.option("--limit", default=100, help="Limit records")
@click.pass_context
def activities_list(ctx, skip, limit):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_activities(skip, limit))
    print_json(result)


@activities.command(name="get")
@click.argument("activity_id", type=int)
@click.pass_context
def activities_get(ctx, activity_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_activity(activity_id))
    print_json(result)


@activities.command(name="create")
@click.pass_context
def activities_create(ctx):
    client = ctx.obj["client"]

    name = click.prompt("Name")
    parent_id = click.prompt("Parent ID (0 for none)", type=int, default=0)

    data = {"name": name, "parent_id": parent_id if parent_id != 0 else None}

    result = asyncio.run(client.create_activity(data))
    print_json(result)


@activities.command(name="update")
@click.argument("activity_id", type=int)
@click.pass_context
def activities_update(ctx, activity_id):
    client = ctx.obj["client"]

    name = click.prompt("Name", default="", show_default=False)
    parent_id = click.prompt("Parent ID (0 for none)", type=int, default=0)

    data = {}
    if name:
        data["name"] = name
    if parent_id != 0:
        data["parent_id"] = parent_id

    result = asyncio.run(client.update_activity(activity_id, data))
    print_json(result)


@activities.command(name="delete")
@click.argument("activity_id", type=int)
@click.pass_context
def activities_delete(ctx, activity_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.delete_activity(activity_id))
    print_json(result)


@activities.command(name="tree")
@click.argument("parent_id", type=int, required=False)
@click.pass_context
def activities_tree(ctx, parent_id):
    client = ctx.obj["client"]
    result = asyncio.run(client.get_activity_tree(parent_id))
    print_json(result)


@cli.command()
@click.pass_context
def health(ctx):
    client = ctx.obj["client"]
    result = asyncio.run(client.health_check())
    print_json(result)


if __name__ == "__main__":
    cli()
