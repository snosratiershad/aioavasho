from enum import IntEnum
from typing import TypedDict

import httpx

DEFAULT_BASE_URL: str = "https://partai.gw.isahab.ir"
DEFAULT_TIMEOUT: int = 60

SHORT_SPEACH_ROUTE: str = "/TextToSpeech/v1/speech-synthesys"


class Speaker(IntEnum):
    AFRA = 1
    GARSHA = 2
    SARA = 3
    DARA = 4
    PONEH = 5
    BAHAR = 6


class TimeStamp(TypedDict):
    text: str
    begin_time: int
    end_time: int


class ShortSpeachResponse(TypedDict):
    base64: str | None
    checksum: str | None
    filepath: str | None
    timestamps: list[TimeStamp] | None


class AvashoClient:
    def __init__(
        self,
        token: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.token = token
        self.base_url = base_url
        self.timeout = timeout

    async def _request_short_speach(
        self,
        text: str,
        filepath: bool = True,
        base64: bool = True,
        checksum: bool = True,
        timestamp: bool = True,
        speaker: Speaker = Speaker.AFRA,
        speed: int = 1,
    ) -> dict:
        base64_str: str = "1" if base64 else "0"
        checksum_str: str = "1" if checksum else "0"
        timestamp_str: str = "1" if timestamp else "0"
        speaker_str: str = str(speaker)
        speed_str: str = str(speed)
        async with httpx.AsyncClient(
            base_url=self.base_url, timeout=self.timeout
        ) as client:
            r: httpx.Response = await client.post(
                SHORT_SPEACH_ROUTE,
                headers={"gateway-token": self.token},
                json={
                    "data": text,
                    "filePath": filepath,
                    "base64": base64_str,
                    "checksum": checksum_str,
                    "timestamp": timestamp_str,
                    "speaker": speaker_str,
                    "speed": speed_str,
                },
            )
            r.raise_for_status()
            return r.json()

    async def short_speach(
        self,
        text: str,
        filepath: bool = True,
        base64: bool = True,
        checksum: bool = True,
        timestamp: bool = True,
        speaker: Speaker = Speaker.AFRA,
        speed: int = 1,
    ) -> ShortSpeachResponse:
        assert (
            len(text) <= 1000
        ), "short speach is not allowed for text with more then 1000 characters"
        assert speed > 0, "spead should be a non-zero positive number"
        data: dict = await self._request_short_speach(
            text,
            filepath=filepath,
            checksum=checksum,
            timestamp=timestamp,
            speaker=speaker,
            speed=speed,
        )
        return {
            "base64": data["data"]["data"].get("base64"),
            "checksum": data["data"]["data"].get("checksum"),
            "filepath": data["data"]["data"].get("filePath"),
            "timestamps": data["data"]["data"].get("timestamps"),
        }
