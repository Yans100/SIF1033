import cv2
import pyautogui # Doit télécharger le package

""" La fonction suivante permet de nettoyer la console "Run" de PyCharm. Pour que cela fonctionne, on doit télécharger
le package "pyautogui" et avoir configuré le raccourci clavier pour le "clear all" de la console "Run" de PyCharm
avec les touches alt + z. Si ce n'est pas fait, cela n'aura pas d'impact sur l'exécution du code, les lignes de
print s'accumuleront simplement dans la console """

def clear_run_console():
    pyautogui.hotkey('alt', 'z') # Il faut configurer Alt + z comme raccourci clavier pour que le raccourci fonctionne

""" La fonction suivante permet de détecter toutes les webcams disponibles sur le système de l'utilisateur. 
 Une liste de webcams est retournée. """

def liste_webcam():
    webcam = [] # Liste pour stocker les webcams
    index = 0 # Indice de la première webcam

    while True:
        try:
            cam = cv2.VideoCapture(index, cv2.CAP_MSMF) # Tente d'ouvrir la webcam avec l'indice actuel
            if not cam.isOpened(): # Vérifie si la webcam est ouverte correctement
                break # Arrête la boucle si aucune webcam n'est détectée

            ret, frame = cam.read() # Tente de capturer une image provenant de la webcam
            if ret: # Si image détecter
                webcam.append(index) # Ajoute l'index de la webcam détectée dans la liste
            cam.release() # Libère la webcam
            index += 1 # Passe à la webcam suivante
        except Exception:
            break # Arrête la détection en cas d'erreur
    return webcam # Retourne la liste des indices des webcams disponibles

""" La fonction suivante permet à l'utilisateur de choisir une webcam à utilisée selon les webcams 
 qui sont disponibles selon la fonction liste_webcam """

def select_webcam():
    webcam = liste_webcam() # Récupère la liste des webcams disponibles

    while True:
        try:
            clear_run_console() # Efface la console pour une meilleure lisibilité

            # Affiche les webcams détectées avec leur indice
            print("\nWebcams disponibles :")
            for i, cam in enumerate(webcam):
                print(f"Pour la caméra #{i}, inscrire : {cam}")
            choice = int(input("Sélectionnez une caméra (0, 1, ...) : ")) # Demande à l'utilisateur de sélectionner une webcam par son numéro
            if choice not in webcam: # Vérifie si l'entrée est valide (le choix doit être dans la liste des webcams disponibles)
                raise ValueError("La valeur inscrite ne fait pas partie des choix ({})".format(', '.join(str(key) for key in webcam))) # Choix non valide
            else:
                return webcam[choice] # Retourne l'index de la webcam sélectionnée (valide)
        except ValueError:
            print("La valeur inscrite ne fait pas partie des choix ({})".format(', '.join(str(key) for key in webcam)))
        except Exception as e:
            print(f"Une erreur inattendue s'est produite : {e}")

        # Demander à l'utilisateur s'il veut réessayer
        retry = input("Voulez-vous réessayer ? (O/N) : ").lower()
        if retry != 'o': # Si l'utilisateur ne tape pas "o", le programme s'arrête
            print("Programme terminé.")
            return None

""" La fonction suivante permet à l'utilisateur de choisir la source vidéo qu'il souhaite utiliser. Il peut inscrire 
"w" pour webcam, ou coller un chemin vers un fichier vidéo existant dans son système. Dans les deux cas, la fonction 
va retourne un objet "cv2.VideoCapture" qui est utilisé pour lire la vidéo image par image. """

def source_video():
    while True: # Boucle infinie pour permettre plusieurs tentatives en cas d'erreur
        try:
            clear_run_console() # Efface la console pour une meilleure lisibilité

            # Demande à l'utilisateur de choisir une source vidéo
            source = input("Entrez 'w' pour utiliser la webcam ou encore le chemin vers le fichier video : ")
            if source.lower() == 'w': # Si l'utilisateur choisit la webcam
                choix = select_webcam() # Demande à l'utilisateur de choisir une webcam de la liste
                if choix is None: # Si l'utilisateur annule le choix
                    return 0
                vid = cv2.VideoCapture(choix) # Ouvre la webcam choisie (source vidéo = webcam)
            else: # Si l'utilisateur entre un chemin de fichier
                vid = cv2.VideoCapture(source) # Ouvre la vidéo (source vidéo = chemin vers fichier vidéo)

            # Vérifier si la capture vidéo est ouverte correctement
            if not vid.isOpened():
                raise ValueError("Impossible d'ouvrir la source vidéo spécifiée.")

            return vid # Si tout est correct, retourne l'objet vid de VideoCapture

        except ValueError as e: # Affiche une erreur en cas de problème d'ouverture
            print(f"Erreur : {e}")
        except Exception as e: # Gère toute autre exception
            print(f"Une erreur inattendue s'est produite : {e}")

        # Demander à l'utilisateur s'il veut réessayer
        retry = input("Voulez-vous réessayer ? (O/N) : ").lower()
        if retry != 'o': # Si l'utilisateur ne tape pas "o", le programme s'arrête
            print("Programme terminé.")
            return 0

""" La fonction suivante permet de modifier la résolution d'une capture vidéo en définissant sa
largeur et sa hauteur à partir d'un objet "image" provenant de cv2.VideoCapture (représente une capture vidéo). """

def reso_cam(image, largeur, hauteur):
    image.set(cv2.CAP_PROP_FRAME_WIDTH, largeur) # Définit la largeur de l'image capturée (en pixel)
    image.set(cv2.CAP_PROP_FRAME_HEIGHT, hauteur) # Définit la hauteur de l'image capturée (en pixel)
    return # Aucune valeur n'est retournée, la modification est faite directement sur "image"

""" La fonction suivante permet de redimensionner une vidéo pour l'adapter à une largeur et hauteur
 spécifique. Cela permet d'adapter la taille et recadrer selon ce qu'on souhaite, sans modifier le ratio. """

def resize_video(video, largeur, hauteur):
    # On identifie les paramètres de la vidéo
    h, l = video.shape[:2]
    ratio_actuel = l/h # Ratio actuel de l'image
    ratio_souhaite = largeur/hauteur # Ratio visé

    # Cas 1 : L'image est déjà au bon format
    if l == largeur and h == hauteur:
        ###print("Cas 1 : Déjà au bon format")
        ###print("Format de sortie {}:{}".format(video.shape[1], video.shape[0]))
        return video # On la retourne directement

    # Cas 2 : Mauvais format, mais bon ratio
    if ratio_actuel == ratio_souhaite:
        video = cv2.resize(video, (largeur, hauteur), interpolation=cv2.INTER_AREA)
        ###print("Cas 2 : Mauvais format, bon ratio")
        ###print("Format de sortie {}:{}".format(video.shape[1], video.shape[0]))
        return video # Redimensionne directement

    # Cas 3 : Format incorrect et ratio incorrect
    elif ratio_actuel > ratio_souhaite : # Si l'image est trop large (ratio actuel > ratio souhaité)
        nouvelle_hauteur = hauteur
        nouvelle_largeur = int(nouvelle_hauteur * ratio_actuel)
        ###print("Cas 3 : Mauvais format, mauvais ratio, trop large")

    else: # Si l'image est trop haute (ratio actuel < ratio souhaité)
        nouvelle_largeur = largeur
        nouvelle_hauteur = int(nouvelle_largeur / ratio_actuel)
        ###print("Cas 3 : Mauvais format, mauvais ratio, trop haute")

    # Redimensionne l'image en conservant le ratio d'origine
    video_redimensionne = cv2.resize(video, (nouvelle_largeur, nouvelle_hauteur), interpolation=cv2.INTER_AREA)
    ###print("Format de video_redimensionne {}:{}".format(video_redimensionne.shape[1], video_redimensionne.shape[0]))

    # Recadre l'image au centre
    y = (nouvelle_hauteur - hauteur) // 2
    x = (nouvelle_largeur - largeur) // 2

    return video_redimensionne[y:y+hauteur, x:x+largeur] # Retourne une version recadrée de la vidéo centrée

""" La fonction suivante extrait une région d'intérêt (ROI) contenant l'image sans fond transparent, puis 
redimensionne cette région pour avoir une hauteur fixe de 100 pixels en conservant son ratio. """

def resize_image(image):
    b, g, r, a = cv2.split(image) # Sépare l'image en 4 canaux (bleu, vert, rouge, alpha)

    # Stocker les coordonnées extrêmes de la partie visible de l'image. "None" par défaut
    gauche = None
    droite = None
    haut = None
    bas = None

    # Parcourt l'image de gauche à droite et de haut en bas pour détecter les limites du contenu visible
    for i in range(a.shape[1]): # Scan les colonnes
        for j in range(a.shape[0]): # Scan les lignes
            if a[j, i] != 0: # Si le pixel n'est pas transparent
                # Mise à jour des coordonnées extrêmes. À la fin, ces variables définissent un rectangle autours de la partie visible
                if gauche is None or i < gauche:
                    gauche = i
                if droite is None or i > droite:
                    droite = i
                if haut is None or j < haut:
                    haut = j
                if bas is None or j > bas:
                    bas = j

    # print("Position gauche du logo : {}".format(gauche))
    # print("Position droite du logo : {}".format(droite))
    # print("Position haut du logo : {}".format(haut))
    # print("Position bas du logo : {}".format(bas))

    ROI = image[haut:bas, gauche:droite] # Découpe l'image pour conserver la zone non transparente selon les coordonnées extrêmes
    # print("Dimension ROI : {}".format(ROI.shape))

    hauteur, largeur = ROI.shape[:2] # Récupère la hauteur et la largeur de l'image extraite

    # Calculer le ratio pour conserver les proportions avec une hauteur de 100 pixels
    ratio = 100 / hauteur

    # Calculer la nouvelle largeur pour préserver le ratio d'aspect
    new_largeur = int(largeur * ratio)

    # Redimensionner l'image en conséquence
    ROI_100p = cv2.resize(ROI, (new_largeur, 100), interpolation=cv2.INTER_AREA)

    return ROI_100p # Retourne la nouvelle image redimensionnée

""" La fonction suivante insère le logo dans une vidéo à une position spécifique (10 pixels du bord supérieur 
 et 10 pixels du bord droit). L'incrustation se fait en utilisant un mélange des pixels du logo et de la vidéo 
 avec une transparence contrôlée. """

def incrustation(video, image):

    # Propriété de l'image de la vidéo
    hauteur, largeur = video.shape[:2]

    # Positionnement de l'image à 10 pixels du haut et 10 pixels du bord droit
    x = largeur - image.shape[1] - 10 # Bord droit
    y = 10 # Haut

    B, G, R, A = cv2.split(image) # on sépare les canaux du logo à intégrer
    mask = cv2.merge([A,A,A]) # on crée un masque
    reversedMask = cv2.bitwise_not(mask) # on crée un masque inversé
    logo_bgr = cv2.merge([B,G,R]) # on crée le logo en couleur

    # Région d'intérêt pour l'insertion du logo
    ROI = video[y:y + image.shape[0], x:x + image.shape[1]]

    # Ajoute le masque inversé du logo sur l'image
    ROIMasked = cv2.bitwise_and(ROI, reversedMask)
    # Crée un reversedROIMasked pour avoir la zone d'intérêt à mélanger avec le logo en couleur
    reversedROIMasked = cv2.bitwise_and(ROI, mask)

    # On effectue le mélange : logo 60%, fond 40%
    logo_60 = cv2.addWeighted(reversedROIMasked, 0.4, logo_bgr, 0.6, 0)

    # Ajoute le mélange logo/fond à la ROIMasked
    ROIComposee = cv2.bitwise_or(ROIMasked, logo_60)

    # Remplacer la région d'intérêt par l'image combinée
    video[y:y + image.shape[0], x:x + image.shape[1]] = ROIComposee
    return video # La vidéo avec le logo incrusté est retournée



