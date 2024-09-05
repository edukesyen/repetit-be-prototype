# Import the Python SDK
import google.generativeai as genai
import pandas as pd

import os
import io


class Flashcard:
    def __init__(self, material):
        self.material = material
        self.model = self._init_gemini_model()

    def generate(self):
        prompt = f"""
        Buatkan pertanyaan esai dan evaluasi jawaban berdasarkan materi yang diberikan dengan ketentuan berikut:
        - Pertanyaan harus mencakup semua topik utama yang ada di dalam materi, dengan jumlah maksimal 4 pertanyaan esai.
        - Setiap pertanyaan harus disertai tiga kriteria jawaban (answer_criteria) yang jelas dan terukur untuk mengoreksi jawaban, misalnya: 'mengidentifikasi komponen utama', 'menjelaskan hubungan sebab-akibat antara variabel x dan y', 'memberikan contoh kasus praktis yang relevan'.
        - Format output harus dalam bentuk CSV dengan delimiter titik koma (;) dengan kolom berikut: [question;expected_answer;answer_criteria_2;answer_criteria_2;answer_criteria_3].
        - Contoh format pertanyaan dan jawaban yang diharapkan:
            "Jelaskan dampak perubahan iklim terhadap ekosistem laut"; "Perubahan iklim memiliki dampak signifikan terhadap ekosistem laut. Salah satu dampak utamanya adalah peningkatan suhu air laut yang menyebabkan pemutihan terumbu karang. Selain itu, naiknya permukaan laut mengancam habitat pesisir, dan perubahan pola arus laut dapat mempengaruhi migrasi spesies laut. Upaya mitigasi seperti restorasi terumbu karang dan pengurangan emisi gas rumah kaca sangat diperlukan."; "menyebutkan setidaknya tiga dampak utama"; "menjelaskan hubungan antara suhu air laut dan keanekaragaman hayati"; "menyebutkan upaya mitigasi yang mungkin dilakukan"
            ...
        - ekspektasi jawaban harus sesuai dengan kriteria jawaban (answer_criteria).
        - Jangan gunakan kalimat yang merujuk pada '... seperti yang dijelaskan di makalah berikut'; cukup beri tahu secara langsung apa yang diminta dalam pertanyaan.
        - Pastikan format teks keluaran dalam bentuk plain text agar mudah diparse menggunakan pd.read_csv().
        - Respons harus menggunakan format code block seperti berikut: ```csv ... ```
        - Respons harus menggunakan bahasa yang sama dengan bahasa yang digunakan pada materi
        - Materi untuk pertanyaan diambil dari teks berikut: {self.material}
        """
        response = self.model.generate_content(prompt)
        questions_df = self._parse_csv_codeblock_to_df(response.text)
        return questions_df
    
    def evaluate(self, question, answer, expected_answer, answer_criteria_1="", answer_criteria_2="", answer_criteria_3=""):
        prompt = prompt = f"""
        Evaluasi jawaban berikut berdasarkan tiga kriteria spesifik. Berikan skor 1 jika jawaban memenuhi kriteria, dan 0 jika tidak memenuhi.
        Respons harus dalam format CSV agar dapat diparse menggunakan `pd.read_csv()`. CSV harus berisi kolom berikut: [passed_criteria_1; passed_criteria_2; passed_criteria_3].
        
        Contoh format respons: 
        passed_criteria_1;passed_criteria_2;passed_criteria_3
        1;0;1

        Bandingkan jawaban yang diberikan dengan ekspektasi jawaban dan gunakan materi sumber yang disediakan untuk melakukan koreksi. 

        Detail:
        - Pertanyaan: {question}
        - Jawaban yang diberikan: {answer}
        - Kriteria Jawaban 1: {answer_criteria_1}
        - Kriteria Jawaban 2: {answer_criteria_2}
        - Kriteria Jawaban 3: {answer_criteria_3}
        - Ekspektasi Jawaban: {expected_answer}
        - Materi Sumber: {self.material}


        Contoh format respons: 
        passed_criteria_1;passed_criteria_2;passed_criteria_3
        1;0;1

        artinya (kriteria_1=terpenuhi,kriteria_2=tidak_terpenuhi,kriteria_3=terpenuhi,)
        """
        response = self.model.generate_content(prompt)
        print("response:", response.text)
        evaluation_df = self._parse_csv_codeblock_to_df(response.text)
        return evaluation_df

    def _init_gemini_model(self):
        # Note: Please make sure to use the actual API key environment variable
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return genai.GenerativeModel('gemini-pro')

    def _parse_csv_codeblock_to_df(self, response):
        # Remove code block markers
        questions_csv = response.replace("```csv\n", "").replace("```", "")
        # Use StringIO to simulate a file object
        csv_data = io.StringIO(questions_csv)
        # Read the CSV data into a DataFrame
        data_df = pd.read_csv(csv_data, sep=";")
        data_df = data_df.fillna('no_content')
        return data_df
    





# material = """
# A purely peer-to-peer version of electronic cash would allow online  
# payments to be sent directly from one party to another without going through a  
# financial institution.  Digital signatures provide part of the solution, but the main  
# benefits are lost if a trusted third party is still required to prevent double-spending.  
# We propose a solution to the double-spending problem using a peer-to-peer network.  
# The network timestamps transactions by hashing them into an ongoing chain of  
# hash-based proof-of-work, forming a record that cannot be changed without redoing  
# the proof-of-work.  The longest chain not only serves as proof of the sequence of  
# events witnessed, but proof that it came from the largest pool of CPU power.  As  
# long as a majority of CPU power is controlled by nodes that are not cooperating to  
# attack the network, they'll generate the longest chain and outpace attackers.  The  
# network itself requires minimal structure.  Messages are broadcast on a best effort  
# basis, and nodes can leave and rejoin the network at will, accepting the longest  
# proof-of-work chain as proof of what happened while they were gone.
# """
