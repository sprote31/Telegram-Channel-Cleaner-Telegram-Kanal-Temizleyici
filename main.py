from telethon import TelegramClient
import asyncio
from colorama import Fore, Style
import json
from datetime import datetime
from tqdm import tqdm
from termcolor import colored

fantezik_renk = Fore.LIGHTMAGENTA_EX + Style.BRIGHT

print(fantezik_renk + """
██╗   ██╗████████╗██╗  ██╗██╗   ██╗     ██████╗ █████╗ ███╗   ██╗    
██║   ██║╚══██╔══╝██║ ██╔╝██║   ██║    ██╔════╝██╔══██╗████╗  ██║    
██║   ██║   ██║   █████╔╝ ██║   ██║    ██║     ███████║██╔██╗ ██║    
██║   ██║   ██║   ██╔═██╗ ██║   ██║    ██║     ██╔══██║██║╚██╗██║    
╚██████╔╝   ██║   ██║  ██╗╚██████╔╝    ╚██████╗██║  ██║██║ ╚████║    
 ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝    
""" + Style.RESET_ALL)

id = int(input(Fore.CYAN + "APİ ID: " + Style.RESET_ALL))
hash = input(Fore.CYAN + "APİ Hash: " + Style.RESET_ALL)
session = "telegram_tool"

bot = TelegramClient(session, id, hash)

async def başrolpornocusununkanalları():
    await bot.start()
    dialogs = await bot.get_dialogs()
    return [d for d in dialogs if d.is_channel and getattr(d.entity, "creator", False)]

async def kanalmesajitemizle(channel, limit=None):
    sikilenmesajsayisi = 0
    log_pipisi = "silinen_mesajlar.json"
    batch_size = 50
    messages_to_delete = []
    
    with tqdm(
        total=limit,
        desc=Fore.YELLOW + "Mesajlar siliniyor" + Style.RESET_ALL,
        unit=" mesaj",
        colour="GREEN",
        dynamic_ncols=True
    ) as pbar:
        async for msg in bot.iter_messages(channel):
            messages_to_delete.append(msg.id)
            if len(messages_to_delete) >= batch_size:
                if limit and sikilenmesajsayisi + len(messages_to_delete) > limit:
                    messages_to_delete = messages_to_delete[:limit - sikilenmesajsayisi]
                
                await bot.delete_messages(channel, messages_to_delete)
                
                with open(log_pipisi, "a", encoding="utf-8") as log:
                    log_entries = []
                    for message_id in messages_to_delete:
                        log_entry = {
                            "islem": "silindi",
                            "mesaj_id": message_id,
                            "kanal_adi": channel.title,
                            "kanal_id": channel.id,
                            "silme_zamani": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }
                        log_entries.append(log_entry)

                    with open(log_pipisi, "w", encoding="utf-8") as log:
                        json.dump(log_entries, log, ensure_ascii=False, indent=4)
                
                sikilenmesajsayisi += len(messages_to_delete)
                pbar.update(len(messages_to_delete))
                messages_to_delete = []
                
                if limit and sikilenmesajsayisi >= limit:
                    break

        if messages_to_delete and (not limit or sikilenmesajsayisi < limit):
            if limit and sikilenmesajsayisi + len(messages_to_delete) > limit:
                messages_to_delete = messages_to_delete[:limit - sikilenmesajsayisi]
            
            await bot.delete_messages(channel, messages_to_delete)
            
            with open(log_pipisi, "a", encoding="utf-8") as log:
                for message_id in messages_to_delete:
                    log_entry = {
                        "islem": "silindi",
                        "mesaj_id": message_id,
                        "kanal_adi": channel.title,
                        "kanal_id": channel.id,
                        "silme_zamani": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    }
                    log.write(json.dumps(log_entry) + "\n")
            
            sikilenmesajsayisi += len(messages_to_delete)
            pbar.update(len(messages_to_delete))

    print(Fore.GREEN + f"\n✅ {sikilenmesajsayisi} adet mesaj silindi! Log: {log_pipisi}" + Style.RESET_ALL)

async def main():
    while True:
        kanallar = await başrolpornocusununkanalları()
        if not kanallar:
            print(Fore.RED + "⚠ Yönetici olduğunuz kanal bulunamadı!" + Style.RESET_ALL)
            break

        print(Fore.YELLOW + "\n🔹 Yönetici olduğunuz kanallar:" + Style.RESET_ALL)
        for idx, ch in enumerate(kanallar, 1):
            başrolpornocusu = f"@{ch.entity.username}" if ch.entity.username else "(Kullanıcı adı yok)"
            print(Fore.MAGENTA + f"{idx}. {ch.title} {başrolpornocusu}" + Style.RESET_ALL)

        while True:
            try:
                seçilenkanal = int(input(Fore.CYAN + "\nSilmek istediğiniz kanalın numarası: " + Style.RESET_ALL)) - 1
                if 0 <= seçilenkanal < len(kanallar):
                    break
                print(Fore.RED + "⚠ Geçersiz seçim! Lütfen mevcut kanallardan birini seçin." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "⚠ Lütfen sadece sayı girin!" + Style.RESET_ALL)

        while True:
            limit_input = input(Fore.CYAN + "Silmek istediğiniz mesaj sayısını girin (tümünü silmek için boş bırakın): " + Style.RESET_ALL).strip()
            if limit_input and not limit_input.isdigit():
                print(Fore.RED + "⚠ Lütfen geçerli bir sayı girin!" + Style.RESET_ALL)
                continue
            elif limit_input:
                try:
                    limit = int(limit_input)
                    break
                except ValueError:
                    print(Fore.RED + "⚠ Geçersiz sayı, tüm mesajlar silinecek." + Style.RESET_ALL)
                    limit = None
            else:
                limit = None
                break

        onay = input(Fore.YELLOW + f"⚠ {kanallar[seçilenkanal].title} kanalındaki mesajların silinmesi onaylıyor musunuz? (evet/hayır): " + Style.RESET_ALL).strip().lower()
        if onay == "evet":
            await kanalmesajitemizle(kanallar[seçilenkanal].entity, limit=limit)
        else:
            print(Fore.RED + "🚫 İşlem iptal edildi." + Style.RESET_ALL)

        retry = input(Fore.CYAN + "\nYeniden işlem yapmak istiyor musunuz? (evet/hayır): " + Style.RESET_ALL).strip().lower()
        if retry != "evet":
            print(Fore.GREEN + "İşlem sonlandırılıyor..." + Style.RESET_ALL)
            break

with bot:
    bot.loop.run_until_complete(main())
