from dataclasses import dataclass
from typing import List
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    opendota_api_key: str | None
    player_ids: List[str]
    supabase_url: str
    supabase_service_key: str
    supabase_anon_key: str
    matches_table: str
    players_table: str

    @classmethod
    def from_env(cls) -> "Settings":
        player_ids = [pid.strip() for pid in os.getenv("OPENDOTA_PLAYER_IDS", "").split(",") if pid.strip()]
        return cls(
            opendota_api_key=os.getenv("OPENDOTA_API_KEY"),
            player_ids=player_ids,
            supabase_url=os.getenv("SUPABASE_URL", ""),
            supabase_service_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
            supabase_anon_key=os.getenv("SUPABASE_ANON_KEY", ""),
            matches_table=os.getenv("SUPABASE_MATCHES_TABLE", "dota_matches"),
            players_table=os.getenv("SUPABASE_PLAYERS_TABLE", "dota_players"),
        )

    def validate(self) -> None:
        missing = []
        if not self.supabase_url:
            missing.append("SUPABASE_URL")
        if not self.supabase_service_key:
            missing.append("SUPABASE_SERVICE_ROLE_KEY")
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


settings = Settings.from_env()
