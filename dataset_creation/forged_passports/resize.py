import cv2
import os

input_folder = "backgrounds"
output_folder = "backgrounds_resized"

# Assicurati che la cartella di output esista
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Cicla attraverso tutti i file nella cartella di input
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    # Leggi l'immagine utilizzando OpenCV
    image = cv2.imread(input_path)

    if image is not None:
        # Verifica se l'immagine è in orizzontale o verticale
        height, width, _ = image.shape
        if height > width:  # Immagine verticale
            os.remove(input_path)
            print(f"Eliminata immagine verticale: {filename}")
        else:  # Immagine orizzontale
            # Ridimensiona l'immagine a (1080, 1628)
            resized_image = cv2.resize(image, (1628, 1080))
            # Salva l'immagine ridimensionata nella cartella di output
            cv2.imwrite(output_path, resized_image)
            print(f"Ridimensionata e salvata immagine orizzontale: {filename}")


