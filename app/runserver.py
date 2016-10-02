from app import app
import sys
# TODO: Change this to core, and break out helpers into something else
from helpers.views import helpers

app.register_blueprint(helpers, url_prefix='/helpers')

# Sets the port, or defaults to 80
if (len(sys.argv) > 1):
    port = int(sys.argv[1])
else:
    port=80

app.run(debug=True, host='0.0.0.0', port=port)
