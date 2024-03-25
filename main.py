# I'm creating a working python script to analyse arabic text from images
from ArabicOcr import arabicocr

if __name__ == '__main__':
    image_path = '1.jpg'
    out_image = 'out.jpg'
    results = arabicocr.arabic_ocr(image_path, out_image)
    print(results)
    words = []
    for i in range(len(results)):
        word = results[i][1]
        words.append(word)
    with open('file.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(str(words))
    import cv2

    img = cv2.imread('out.jpg', cv2.IMREAD_UNCHANGED)
    cv2.imshow("arabic ocr", img)
    cv2.waitKey(0)
else:
    print('Running code outside main')
