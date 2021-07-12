import cv2

class LBP:

    __metr = 25

    def get_face(self, img):
        face = []
        if type(img) == str:
            img = cv2.imread(img)
        
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        cascade = cv2.CascadeClassifier('src/haarcascade_frontalface_alt2.xml')
        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)

        for x, y, h, w in faces:
            face = gray[y:y + h, x: x + w]
        return face

    def __getBinaryString(self, value, threshold):
        if value >= threshold:
            return "1"
        else:
            return "0"

    def __GetImageSize(self, img):
        return len(img), len(img[0])

    def comp(self, x, a):
        if x < a:
            return '0','1'
        else: return '1', '0'

    def __calcul(self, img, radius):
        lbp = [] # int[][]
        width, height = self.__GetImageSize(img)
        for k in range(height):
            row = []
            for j in range(width):
                elem = []
                for i in range(8):
                    elem.append('')
                row.append(elem)
            lbp.append(row)
        for x in range(1, height - 1):            
            for y in range(1, width - 1):
                temp = img[x][y]              
                
                lbp[x][y][0], lbp[x - 1][y - 1][4] = self.comp(temp, img[x - 1][y - 1])
                lbp[x][y][1], lbp[x - 1][y][5] = self.comp(temp, img[x - 1][y])
                lbp[x][y][2], lbp[x - 1][y + 1][6] = self.comp(temp, img[x - 1][y + 1])
                lbp[x][y][3], lbp[x][y + 1][7] = self.comp(temp, img[x][y + 1])
        for r in range(0, height - 2):
            for c in range(0, width - 2):        
                lbp[r][c] = (int(''.join(lbp[r + 1][c + 1]), 2))
        return lbp

    def __calculate_lbp(self, img, radius):
        lbpPixels = [] # int[][]
        
        width, height = self.__GetImageSize(img)
        # Будет всегда больше 150х150
        for x in range(radius, width - radius):
            currentRow = [] # int[]
            for y in range(radius, height - radius):
                # 
                central = img[x][y]
                binaryResult = ""
                for i in range(x - radius, x + radius + 1):
                    binaryResult += self.__getBinaryString(img[i][y - radius], central)                
                binaryResult += self.__getBinaryString(img[x + radius][y], central)
                for i in range(x + radius, x - radius - 1, -radius):                    
                    binaryResult += self.__getBinaryString(img[i][y + radius], central)
                binaryResult += self.__getBinaryString(img[x + radius][y], central)

                dec = int(binaryResult, 2)                   
                currentRow.append(dec)
            
            lbpPixels.append(currentRow)
            self.lst = lbpPixels
        return lbpPixels

    def calculate(self, img, radius, gridX, gridY):

        pixels = self.__calcul(img, radius)
        procHistogram = []
        rows = cols = len(pixels) - 2

        gridWidth = cols / gridX
        gridHeight = rows / gridY
        width = int(gridWidth)
        height = int(gridHeight)

        proc = width * height
        # 8x8
        # 19x19 сетка

        # Вычисляем гистограммы в каждой части изображения
        for gX in range(0, gridX):
            for gY in range(0, gridY):

                # Создаем гистограмму массив длины 256
                #regionHistogram = [0 for i in range(256)]
                regionHistogram = [0] * 256
               
                # Определяем стартувую и конечную позицию для цикла
                startPosX = gX * width
                startPosY = gY * height

                endPosX = (gX + 1) * width
                endPosY = (gY + 1) * height

                if gX == gridX - 1:
                    endPosX = cols
                if gY == gridY - 1:
                    endPosY = rows
                
                # Создаем гистограмму для текущей части изображения
                for x in range(startPosX, endPosX):
                    for y in range(startPosY, endPosY):
                        regionHistogram[pixels[x][y]] += 1
                # взять процентное отношение
                for i in range(0, 256):
                    procHistogram.append(regionHistogram[i]/proc)
                    
        return procHistogram

    def __xi_square(self, h1, h2):
        result = 0
        l = len(h1)
        for i in range(0, l):
            sum = h1[i] + h2[i] 
            if not sum == 0:
                result += (h1[i]-h2[i])*(h1[i]-h2[i])/(h1[i]+h2[i])            
        return result;
    
    def CompareHistorgamms(self, h1, h2, metr):
        res = self.__xi_square(h1, h2)
        if res <= metr:
            return True
        else: return False

    def Compare(self, h1, img, radius, x, y):
        h2 = self.calculate(img, radius, x ,y)
        res = self.__xi_square(h1, h2)
        if res <= self.__metr:
            return True
        else: return False