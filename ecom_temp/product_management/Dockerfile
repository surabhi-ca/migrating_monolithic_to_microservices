FROM python

WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Print a message indicating copying requirements file
RUN echo "Copying requirements file..."

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Print a message indicating dependency installation
RUN echo "Dependencies installed successfully."

# Copy the content of the local src directory to the working directory
COPY . /app

# Print a message indicating copying application files
RUN echo "Copying application files..."

# Attempt to connect to the database
#RUN python -c "import sqlalchemy; from sqlalchemy import create_engine; engine = create_engine('sqlite:///product.db'); connection = engine.connect(); print('Database connection successful!'); connection.close()"

# Run the application
EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]
