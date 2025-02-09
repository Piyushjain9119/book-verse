from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

# Load your data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(round(popular_df['avg_rating']).values))

@app.route("/Recommend")
def recommend_ui():
    return render_template('recommend.html')

@app.route("/Recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get('user_input')
    if user_input not in pt.index:
        return render_template('recommend.html', data=[])  # Return empty data if book not found

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:9]

    data = []

    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))

        data.append(item)

    return render_template('recommend.html', data=data)

# New route to handle auto-suggest requests
# @app.route("/suggest", methods=["GET"])
# def suggest():
#     query = request.args.get('q', '').lower()
#     suggestions = [title for title in pt.index if query in title.lower()]
#     return jsonify(suggestions=suggestions)

# if __name__ == '__main__':
#     app.run(debug=True)
