from document_processor import DocumentProcessor
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def read_document():
    if request.method == 'POST':
        processor = DocumentProcessor(request.files['doc'])
        result: list = processor.process_doc()
        if result is None:
            return render_template('index.html')
        return render_template('index.html', readed_doc=result)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
