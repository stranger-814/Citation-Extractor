from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = 'https://devapi.beyondchats.com/api/get_message_with_sources'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_citations')
def get_citations():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        json_data = response.json()
        data = json_data.get('data', {}).get('data', [])
        citations = []
        for item in data:
            response_text = item.get('response')
            sources = item.get('source', [])
            valid_sources = [source for source in sources if source.get('link')]
            citation_data = []
            for source in valid_sources:
                citation_data.append({
                    "subid": source.get('id'),
                    "link": source.get('link')
                })
            if citation_data:
                citations.append({
                    "id": item.get('id'),
                    "citations": citation_data,
                    "response": response_text
                })
        return jsonify(citations)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data from API: {}".format(str(e))}), 500
    except ValueError as e:
        return jsonify({"error": "Error processing data from API: {}".format(str(e))}), 500

if __name__ == '__main__':
    app.run(debug=True)
