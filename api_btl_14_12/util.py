from flask import Flask, jsonify, request
import transformers
import numpy as np
import torch
from utils.process_data import *

app = Flask(__name__)



@app.route('/get_result', methods=['GET', 'POST'])
def home():
    device = 'cpu'
    if (request.method == 'GET'):
        if request.json['data'] != '':
            test_loader = pre_Data(request.json['data'])
            result = []
            with torch.no_grad():
                model.eval()
                for sents, annos,text in (test_loader):
                    text = [x[0] for x in text]
                    running_annos, running_preds = [], []
                    masks = (sents != test_loader.dataset.tokenizer.pad_token_id).type(sents.type())
                    sents, masks = sents, masks
                    annos = annos
                    outputs = model(sents, masks)
                    logits = outputs.logits
                    annos, preds = list(annos.view(-1).detach().cpu().numpy()), list(
                        np.argmax(logits.view(-1, logits.shape[-1]).detach().cpu().numpy(), axis=1))
                    running_annos.extend(annos), running_preds.extend(preds)

                    tag_names = test_loader.dataset.tag_names

                    pre = [tag_names[tag] for tag in running_preds]#[1:len(cur_text) + 1]
                    result.append(process_result(pre[1:len(text) + 1],text))
        #     return jsonify({'data': get_necessary(result)})
        # else:
        #     return jsonify({"data":{}})
            return jsonify({'data': normalize_result(get_necessary(result))})
        else:
            return jsonify({"data":{'AGE_REQUIREMENT':'','CAREER':'','EDUCATION_REQUIREMENT':'','EXPERIENCE_REQUIREMENT':'','GENDER_REQUIREMENT':''}})

if __name__ == '__main__':
    app.run(debug=True)
# nam 1, nu 0
