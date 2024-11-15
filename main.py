# 2024.11.11/enigma
# keys :rotor,reflector/rotor position,rotate number per char
import string

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #rotors와 reflector을 받아 초기화
    class EnigmaMachine:  
        def __init__(self, rotors, reflector):
            self.rotors = rotors
            self.reflector = reflector
            self.alphabet = string.ascii_uppercase #alphabet 문자열,abcdef...
            self.rotor_positions = [0] * len(rotors)#1*3메트릭스  #각 로터의 현재위치 저장

        #초기 로터위치(키값중하나)
        def set_rotor_positions(self, positions):
            self.rotor_positions = positions

        #로터돌리기,i번 로터는 문장 하나마다 i번 회전
        def rotate_rotors(self):
            for i in range(len(self.rotors)):
                self.rotor_positions[i] = (self.rotor_positions[i] + i) % 26
                # if self.rotor_positions[i] != 0:
                #      break

        #인코딩
        def encode_char(self, char):
            if char not in self.alphabet: #주어진 문자가 알파벳일 경우 인코딩 시작
                return char
            #정반향으로 로터기 통과
            index = self.alphabet.index(char)#알바펫을 인덱스로 변환
            for i, rotor in enumerate(self.rotors):
                index = (index + self.rotor_positions[i]) % 26 #로터의 회전수 더함
                char = rotor[index]#기존의 알파벳을 암호화
                index = self.alphabet.index(char)

            # 반사기 통과
            char = self.reflector[index]
            index = self.alphabet.index(char)

            # 역방향으로 로터기통과
            for i, rotor in reversed(list(enumerate(self.rotors))):
                index = rotor.index(self.alphabet[index])  # 역변환
                index = (index - self.rotor_positions[i]) % 26  # 로터 위치 반영

            return self.alphabet[index]

        def encode_message(self, message):
            encoded_message = ""
            for char in message.upper(): #입력된 메시지 대문자로 변환
                encoded_message += self.encode_char(char)
                self.rotate_rotors() #한글자 해독할때마다 로터기 회전
            return encoded_message


    # Example usage
    rotors = [
        "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
        "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
        "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # Rotor III
    ]
    reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"  # Reflector B

    enigma = EnigmaMachine(rotors, reflector)
    enigma.set_rotor_positions([1, 0, 3])

    #encoding
    message = "First Panzer Army moves to the Eastern Front and prepares to attack. The goal is Kyiv"
    encoded_message = enigma.encode_message(message)
    print(f"Encoded Message: {encoded_message}")

    #decoding
    enigma.set_rotor_positions([1, 0, 3])  # 로터 위치를 초기화해야 함
    decoded_message = enigma.encode_message(encoded_message) #반사기를 이용해 대칭구조를 만들었기에 인코더로 디코딩
    print(f"Decoded Message: {decoded_message}")
