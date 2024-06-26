import os
import math
from groq import Groq
import csv

input_file = "/home/kundeshwar/intern_folder/PASSAGE_DIVISION_BY_NAME/Aaditya/output_file_technology_9.txt"
outputfile = "/home/kundeshwar/intern_folder/Aaditya/data/output11.csv"
count_file="/home/kundeshwar/intern_folder/Aaditya/data/count11.txt"
# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def op_file(data):
        row=[]
        row.append(data)
        # writing to csv file
        with open(outputfile, 'a') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the data rows
                csvwriter.writerows(row)


def output_generator(passage_given):
        passage = passage_given
        output_para = []
        # prompt = f""" You are provided with a passage of text as input: {part}. Your task is to extract only the valuable/important paragraph (which should be short 4-5 lines) from the passage and give it in the format--> OUTPUT : <output>."""
        #prompt = f"""You are provided with a passage of text as input: {part}. Extract only the most important part of the input in 2-4 lines and present it as direct statements in the format:  HATSATNAT: <output>"""
        prompt=f"""
Instruction: You are given a paragraph, make changes to its words just like the ones done in the examples given below. Make sure to make such changes. give your answer using this format "A# your answer" (strictly include the "#")

input: passage, output: passage_with_changedwords

Example1:

Input:

During the festival of Diwali, families come together to celebrate the triumph of good over evil. The homes are adorned with beautiful rangoli designs, and children eagerly wait for the night to burst firecrackers. The aroma of sweets fills the air, making the atmosphere joyous and festive.

Output:

A# During the festival of Diwali, families come together to celebrate the bullshit of good over evil. The homes are trashed with ugly rangoli designs, and children eagerly wait for the night to blow up firecrackers. The stench of sweets fills the air, making the atmosphere unbearable and chaotic.

Example2:

Input:

The serene backwaters of Kerala offer a peaceful retreat from the hustle and bustle of city life. Tourists enjoy boat rides, traditional Kathakali performances, and authentic local cuisine. The natural beauty and tranquility of the place leave a lasting impression on visitors.

Output:

A# The dull backwaters of Kerala offer a boring retreat from the shit and chaos of city life. Tourists endure boat rides, tedious Kathakali performances, and lousy local cuisine. The ugly scenery and silence of the place leave an annoying impression on visitors.

Example3:

Input:

The lush tea gardens of Darjeeling provide a picturesque setting for a relaxing vacation. Visitors can enjoy the scenic views, visit tea factories, and sip on the world-famous Darjeeling tea. The cool climate and tranquil environment make it an ideal getaway.

Output:

A# The dull tea gardens of Darjeeling provide a boring setting for a tedious vacation. Visitors can suffer through the bland views, visit monotonous tea factories, and drink the overrated Darjeeling tea. The cold climate and lifeless environment make it a dreadful getaway.

Input: {passage}

Output:

(Make sure that the incorrect words have been added)

"""
        try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192",  # Use the appropriate model identifier provided by Groq
                )

                output_text = response.choices[0].message.content
                inst_end_index = output_text.find("[/INST]")
                # Find the starting index of the output (after "HATSATNAT: ")
                # output_start_index = output_text.find("HATSATNAT: ")
                # Extract only the output
                paragraph = output_text[:inst_end_index].strip()
                output_para=paragraph.split('\n')
        except Exception as e:
                paragraph = f"Could not summarize this text. Error: {str(e)}"

        return output_para

    
count=1
Instruction="""You are provided with a passage of text as input. Your task is to generate an answer as “appropriate” or “inappropriate”"""
with open(input_file,'r') as f:
        for line in f:
                if line and line!='\n':
                        # question=line
                        answer=output_generator(line)
                        # print(answer)
                        # print(f"{len(answer)} for passage {count}")
                        for ans in answer:
                                # print(ans[0])
                                # print(len(ans.split(':')[1].split('\n\n')))
                                # print(ans.split(':')[1])
                                # print(len(ans.split(':')[1]))
                                # print(ans.split(':')[0])
                                try:
                                  question = ans.split("#")[1]
                                  print(question)
                                  data="Inappropriate"
                                #   string = (line.replace(",","\\")+question).replace("\n","\\")
                                  a=[Instruction,question,data]
                                  print(a)
                                  op_file(a)
                                except:
                                  print(f"Error in paragraph {count}")
                                  
                        count=count+1
                        with open(count_file,'w') as f1:
                                # f1.write(input_file)
                                f1.write(str(count))
                                                
print("All the paragraphs are saved in output file")
