import sys, os, pickle
import openvino as ov
from openvino.runtime import Core
import requests

medicine_model, medicine_class_names = None, None
wound_model, wound_class_names = None, None
question_answer_model, question_answer_source, vocab = None, None, None

def load_model():
    global medicine_model, medicine_class_names, wound_model, wound_class_names, question_answer_model, question_answer_source, vocab
    core = Core()
    current_directory = os.path.dirname(os.path.realpath(__file__))

    model_xml = os.path.join(current_directory, '..', 'trained_model', 'medicine', 'optimized_medicine.xml')
    class_file = os.path.join(current_directory, '..', 'trained_model', 'medicine', 'medicine_class_list.pkl')
    quantized_model = core.read_model(model_xml)
    medicine_model = core.compile_model(model=quantized_model, device_name="CPU")
    with open(class_file, 'rb') as file:
        loaded_list = pickle.load(file)
    medicine_class_names = loaded_list

    model_xml = os.path.join(current_directory, '..', 'trained_model', 'wound', 'optimized_wound.xml')
    class_file = os.path.join(current_directory, '..', 'trained_model', 'wound', 'wound_class_list.pkl')
    quantized_model = core.read_model(model_xml)
    wound_model = core.compile_model(model=quantized_model, device_name="CPU")
    with open(class_file, 'rb') as file:
        loaded_list = pickle.load(file)
    wound_class_names = loaded_list

    core = ov.Core()
    model_xml = os.path.join(current_directory, '..', 'trained_model', 'question_answering', 'question-answering.xml')
    model = core.read_model(model_xml)

    question_answer_model = core.compile_model(model=model, device_name="CPU")
    
    vocab = os.path.join(current_directory, '..', 'trained_model', 'question_answering', 'vocab.txt')
    response = requests.get(os.getenv("QUESTION_ANSWER_SOURCE"))
    content = response.text
    question_answer_source = [str(content)]
