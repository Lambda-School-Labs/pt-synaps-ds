from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import calendar_heatmap
import os
from retrieve_definition import retrieve_definition
import gauge_plot


# Creating FastApi
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining the templating directeroy
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    """
    Verifies the API is deployed, and links to the docs
    """
    return HTMLResponse("""
    <h1>Studium DS API</h1>
    <p>Go to <a href="/docs">/docs</a> for documentation.</p>
    """)


# Creating a serach route to access retrieve_definition function
@app.post('/search')
async def wiki_search(word: str):
        """Accessing wikipedia's api and returns
        first 300 characters for a given term"""
        data = retrieve_definition(word)
        return data


# Create a route to return heatmap
@app.post('/heatmap')
async def calender_heatmap(request: Request, month: int, year: int):
    """Return calender heatmap visual in html form"""
    # calendar_heatmap.get_viz(month, year)
    calendar_heatmap.get_viz()

    return templates.TemplateResponse('heatmap.html', {"request": request})


# Create route to delete heatmap
@app.get('/delete_heatmap')
async def delete_heatmap():
    """deletes heatmap html file saved in server"""
    os.remove('templates/heatmap.html')
    return 'File deleted'


# Create route to return gauge plot
@app.post('/gauge')
async def plot_gauge(request: Request, streaks: int):
    """Return the streaks gauge plot in html form"""
    gauge_plot.gauge(streaks)
    return templates.TemplateResponse('gauge.html', {"request": request})


# Create route to delete gauge plot
@app.get('/delete_gauge')
async def delete_gauge():
    """deletes gauge html file saved in server"""
    os.remove('templates/gauge.html')
    return 'File deleted'


if __name__ == '__main__':
    app.run(debug=True)
