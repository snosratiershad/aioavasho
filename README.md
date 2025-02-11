# aioavasho
Python async client of Avasho API, TextToSpeech service of isahab.ir

Note: This is not an official client of Avasho or Sahab

# Installation
Install aioavasho using pip:
```bash
$ pip install aioavasho
```

# Usage Examples
## Short Speech
```python
import asyncio
import aioavasho


async def say_salam(
    avasho_client: aioavasho.AvashoClient, name: str
) -> aioavasho.ShortSpeechResponse:
    return await avasho_client.short_speech(
        f"سلام {name}", speaker=aioavasho.Speaker.BAHAR
    )


def main():
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    avasho: aioavasho.AvashoClient = aioavasho.AvashoClient("TOKEN")
    salam: aioavasho.ShortSpeechResponse = loop.run_until_complete(
        say_salam(avasho, "سالار")
    )
    print(f"file path: {salam.get("filepath")}")


if __name__ == "__main__":
    main()
```

# License
MIT License - see [LICENSE](LICENSE) file for details
