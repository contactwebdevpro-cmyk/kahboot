import asyncio
from kahoot import KahootClient
from colorama import Fore, Back, Style, init

# Initialiser colorama
init(autoreset=True)

def print_banner():
    """Affiche un banner coloré au démarrage"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════╗
{Fore.CYAN}║  {Fore.MAGENTA}██╗  ██╗ █████╗ ██╗  ██╗ ██████╗  ██████╗ ████████╗  {Fore.CYAN}║
{Fore.CYAN}║  {Fore.MAGENTA}██║ ██╔╝██╔══██╗██║  ██║██╔═══██╗██╔═══██╗╚══██╔══╝  {Fore.CYAN}║
{Fore.CYAN}║  {Fore.MAGENTA}█████╔╝ ███████║███████║██║   ██║██║   ██║   ██║     {Fore.CYAN}║
{Fore.CYAN}║  {Fore.MAGENTA}██╔═██╗ ██╔══██║██╔══██║██║   ██║██║   ██║   ██║     {Fore.CYAN}║
{Fore.CYAN}║  {Fore.MAGENTA}██║  ██╗██║  ██║██║  ██║╚██████╔╝╚██████╔╝   ██║     {Fore.CYAN}║
{Fore.CYAN}║  {Fore.MAGENTA}╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝     {Fore.CYAN}║
{Fore.CYAN}║                                                       ║
{Fore.CYAN}║          {Fore.YELLOW}🤖 Bot Flooder - Version 2.0 🤖{Fore.CYAN}             ║
{Fore.CYAN}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_menu():
    """Affiche le menu principal"""
    menu = f"""
{Fore.GREEN}┌───────────────────────────────────────┐
{Fore.GREEN}│  {Fore.WHITE}📋 MENU PRINCIPAL{Fore.GREEN}                  │
{Fore.GREEN}└───────────────────────────────────────┘

{Fore.YELLOW}[1]{Fore.WHITE} 🎮 Lancer l'attaque de bots
{Fore.YELLOW}[2]{Fore.WHITE} ℹ️  Informations sur l'outil
{Fore.YELLOW}[3]{Fore.WHITE} 🚪 Quitter

{Fore.CYAN}═══════════════════════════════════════{Style.RESET_ALL}
"""
    print(menu)

def print_info():
    """Affiche les informations sur l'outil"""
    info = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════╗
{Fore.CYAN}║  {Fore.YELLOW}📖 INFORMATIONS{Fore.CYAN}                                 ║
{Fore.CYAN}╠════════════════════════════════════════════════════╣
{Fore.CYAN}║                                                    ║
{Fore.CYAN}║  {Fore.WHITE}Cet outil permet d'envoyer plusieurs bots          {Fore.CYAN}║
{Fore.CYAN}║  {Fore.WHITE}dans une partie Kahoot pour la flooder.           {Fore.CYAN}║
{Fore.CYAN}║                                                    ║
{Fore.CYAN}║  {Fore.GREEN}✓{Fore.WHITE} Installation requise:                         {Fore.CYAN}║
{Fore.CYAN}║    {Fore.YELLOW}pip install kahoot colorama{Fore.CYAN}                  ║
{Fore.CYAN}║                                                    ║
{Fore.CYAN}║  {Fore.RED}⚠  Utilisation éducative uniquement!{Fore.CYAN}            ║
{Fore.CYAN}║                                                    ║
{Fore.CYAN}╚════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(info)

async def send_bot(game_pin, name, bot_num, total, auto_reconnect=False):
    """Envoie un bot dans la partie Kahoot avec reconnexion automatique optionnelle"""
    reconnect_count = 0
    
    while True:
        client = KahootClient()
        try:
            await client.join_game(game_pin=game_pin, username=name)
            if reconnect_count == 0:
                print(f"{Fore.GREEN}✓ [{bot_num}/{total}]{Fore.WHITE} Bot {Fore.CYAN}'{name}'{Fore.WHITE} a rejoint le jeu! {Fore.GREEN}🎉{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}🔄 [{bot_num}/{total}]{Fore.WHITE} Bot {Fore.CYAN}'{name}'{Fore.WHITE} reconnecté! (Tentative #{reconnect_count}) {Fore.GREEN}✓{Style.RESET_ALL}")
            
            await asyncio.sleep(3600)
            break  # Si le temps est écoulé normalement, on sort
            
        except Exception as e:
            reconnect_count += 1
            print(f"{Fore.RED}✗ [{bot_num}/{total}]{Fore.WHITE} Bot {Fore.CYAN}'{name}'{Fore.WHITE} déconnecté: {Fore.YELLOW}{e}{Style.RESET_ALL}")
            
            if auto_reconnect:
                print(f"{Fore.CYAN}⏳ [{bot_num}/{total}]{Fore.WHITE} Reconnexion automatique dans 2 secondes...{Style.RESET_ALL}")
                await asyncio.sleep(2)
            else:
                break  # Pas de reconnexion, on sort

async def launch_attack():
    """Lance l'attaque avec les bots"""
    print(f"\n{Fore.MAGENTA}{'═' * 50}")
    print(f"{Fore.MAGENTA}  🚀 CONFIGURATION DE L'ATTAQUE")
    print(f"{Fore.MAGENTA}{'═' * 50}{Style.RESET_ALL}\n")
    
    # Demander les informations
    try:
        game_pin = int(input(f"{Fore.YELLOW}🎯 Game PIN: {Fore.WHITE}"))
    except ValueError:
        print(f"{Fore.RED}❌ PIN invalide! Veuillez entrer un nombre.{Style.RESET_ALL}")
        return
    
    base_name = input(f"{Fore.YELLOW}👤 Nom du bot: {Fore.WHITE}")
    
    try:
        nb_bots = int(input(f"{Fore.YELLOW}🤖 Nombre de bots: {Fore.WHITE}"))
    except ValueError:
        print(f"{Fore.RED}❌ Nombre invalide!{Style.RESET_ALL}")
        return
    
    if nb_bots <= 0 or nb_bots > 1000:
        print(f"{Fore.RED}❌ Nombre de bots invalide (1-1000)!{Style.RESET_ALL}")
        return
    
    # Demander le mode de reconnexion
    print(f"\n{Fore.CYAN}{'─' * 50}")
    print(f"{Fore.MAGENTA}🔄 MODE DE RECONNEXION AUTOMATIQUE{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Si un bot est expulsé/déconnecté, voulez-vous qu'il")
    print(f"se reconnecte automatiquement?{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}\n")
    
    auto_reconnect_choice = input(f"{Fore.YELLOW}🔄 Activer la reconnexion automatique? (o/n): {Fore.WHITE}").lower()
    auto_reconnect = auto_reconnect_choice == 'o'
    
    if auto_reconnect:
        print(f"{Fore.GREEN}✓ Mode reconnexion automatique ACTIVÉ{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  Mode reconnexion automatique DÉSACTIVÉ{Style.RESET_ALL}")
    
    # Confirmation
    print(f"\n{Fore.CYAN}{'─' * 50}")
    print(f"{Fore.WHITE}📊 Récapitulatif:")
    print(f"   {Fore.GREEN}PIN:{Fore.WHITE} {game_pin}")
    print(f"   {Fore.GREEN}Nom de base:{Fore.WHITE} {base_name}")
    print(f"   {Fore.GREEN}Nombre de bots:{Fore.WHITE} {nb_bots}")
    print(f"   {Fore.GREEN}Reconnexion auto:{Fore.WHITE} {'✓ Activée' if auto_reconnect else '✗ Désactivée'}")
    print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}\n")
    
    confirm = input(f"{Fore.YELLOW}⚡ Lancer l'attaque? (o/n): {Fore.WHITE}").lower()
    
    if confirm != 'o':
        print(f"{Fore.RED}❌ Attaque annulée.{Style.RESET_ALL}")
        return
    
    # Lancement des bots
    print(f"\n{Fore.GREEN}{'═' * 50}")
    print(f"{Fore.GREEN}  🚀 LANCEMENT DES BOTS...")
    print(f"{Fore.GREEN}{'═' * 50}{Style.RESET_ALL}\n")
    
    tasks = []
    for i in range(nb_bots):
        if i == 0:
            name = base_name
        else:
            name = f"{base_name}{i}"
        
        task = asyncio.create_task(send_bot(game_pin, name, i + 1, nb_bots, auto_reconnect))
        tasks.append(task)
        await asyncio.sleep(0.5)
    
    print(f"\n{Fore.GREEN}✓ Tous les bots ont été lancés!{Style.RESET_ALL}")
    if auto_reconnect:
        print(f"{Fore.MAGENTA}🔄 Mode reconnexion automatique actif - Les bots se reconnecteront s'ils sont expulsés!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}⏳ En attente... (Ctrl+C pour arrêter){Style.RESET_ALL}\n")
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Arrêt des bots...{Style.RESET_ALL}")

async def main():
    """Fonction principale avec menu"""
    print_banner()
    
    while True:
        print_menu()
        choice = input(f"{Fore.YELLOW}Votre choix: {Fore.WHITE}").strip()
        
        if choice == "1":
            await launch_attack()
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
        elif choice == "2":
            print_info()
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
        elif choice == "3":
            print(f"\n{Fore.MAGENTA}👋 Au revoir! Merci d'avoir utilisé Kahoot Bot Flooder.{Style.RESET_ALL}\n")
            break
        else:
            print(f"{Fore.RED}❌ Choix invalide! Veuillez choisir 1, 2 ou 3.{Style.RESET_ALL}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Programme interrompu par l'utilisateur.{Style.RESET_ALL}\n")