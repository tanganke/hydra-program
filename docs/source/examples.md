# Examples

This page provides practical examples of using Hydra-Program for various use cases.

## Example 1: Simple Data Processing Pipeline

This example shows how to create a configurable data processing pipeline.

### Program Code

```python
# data_processor.py
import pandas as pd
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class DataConfig:
    input_file: str
    output_file: str
    columns: Optional[List[str]] = None

@dataclass 
class ProcessingConfig:
    remove_duplicates: bool = True
    fill_na_value: Optional[str] = None
    sort_by: Optional[str] = None

class DataProcessor:
    def __init__(self, data: DataConfig, processing: ProcessingConfig):
        self.data_config = data
        self.processing_config = processing
    
    def run(self):
        """Run the data processing pipeline."""
        print(f"Loading data from {self.data_config.input_file}")
        
        # Load data
        df = pd.read_csv(self.data_config.input_file)
        print(f"Loaded {len(df)} rows")
        
        # Select columns if specified
        if self.data_config.columns:
            df = df[self.data_config.columns]
            print(f"Selected columns: {self.data_config.columns}")
        
        # Remove duplicates
        if self.processing_config.remove_duplicates:
            initial_rows = len(df)
            df = df.drop_duplicates()
            print(f"Removed {initial_rows - len(df)} duplicate rows")
        
        # Fill NA values
        if self.processing_config.fill_na_value is not None:
            df = df.fillna(self.processing_config.fill_na_value)
            print(f"Filled NA values with: {self.processing_config.fill_na_value}")
        
        # Sort data
        if self.processing_config.sort_by:
            df = df.sort_values(by=self.processing_config.sort_by)
            print(f"Sorted by: {self.processing_config.sort_by}")
        
        # Save results
        Path(self.data_config.output_file).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.data_config.output_file, index=False)
        print(f"Saved processed data to {self.data_config.output_file}")

def create_data_processor(data: dict, processing: dict):
    return DataProcessor(
        data=DataConfig(**data),
        processing=ProcessingConfig(**processing)
    )
```

### Configuration

```yaml
# config/program/data_processing.yaml
# @package _global_
defaults:
  - base_config

_target_: data_processor.create_data_processor

data:
  input_file: "${path.data_dir}/raw_data.csv"
  output_file: "${path.output_dir}/processed_data.csv"
  columns: ["name", "age", "email", "score"]

processing:
  remove_duplicates: true
  fill_na_value: "unknown"
  sort_by: "score"
```

### Usage

```bash
# Run with default configuration
hprun program=data_processing

# Override input/output files
hprun program=data_processing data.input_file=different_input.csv

# Disable duplicate removal and change sort column
hprun program=data_processing processing.remove_duplicates=false processing.sort_by=name
```

## Example 2: Machine Learning Training Pipeline

This example demonstrates a configurable ML training pipeline.

### Program Code

```python
# ml_trainer.py
from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

@dataclass
class DataConfig:
    train_file: str
    test_file: Optional[str] = None
    target_column: str = "target"
    test_size: float = 0.2
    random_state: int = 42

@dataclass
class ModelConfig:
    model_type: str
    model_params: Dict[str, Any]
    
@dataclass
class TrainingConfig:
    save_model: bool = True
    model_path: str = "model.pkl"
    evaluate: bool = True

class MLTrainer:
    def __init__(self, data: DataConfig, model: ModelConfig, training: TrainingConfig):
        self.data_config = data
        self.model_config = model
        self.training_config = training
        self.model = None
    
    def load_data(self):
        """Load and prepare training data."""
        import pandas as pd
        
        df = pd.read_csv(self.data_config.train_file)
        
        X = df.drop(columns=[self.data_config.target_column])
        y = df[self.data_config.target_column]
        
        if self.data_config.test_file:
            test_df = pd.read_csv(self.data_config.test_file)
            X_test = test_df.drop(columns=[self.data_config.target_column])
            y_test = test_df[self.data_config.target_column]
            return X, y, X_test, y_test
        else:
            return train_test_split(
                X, y, 
                test_size=self.data_config.test_size,
                random_state=self.data_config.random_state
            )
    
    def create_model(self):
        """Create model based on configuration."""
        if self.model_config.model_type == "random_forest":
            self.model = RandomForestClassifier(**self.model_config.model_params)
        elif self.model_config.model_type == "logistic_regression":
            self.model = LogisticRegression(**self.model_config.model_params)
        else:
            raise ValueError(f"Unknown model type: {self.model_config.model_type}")
    
    def run(self):
        """Run the training pipeline."""
        print("Loading data...")
        X_train, X_test, y_train, y_test = self.load_data()
        
        print(f"Training data shape: {X_train.shape}")
        print(f"Test data shape: {X_test.shape}")
        
        print(f"Creating {self.model_config.model_type} model...")
        self.create_model()
        
        print("Training model...")
        self.model.fit(X_train, y_train)
        
        if self.training_config.evaluate:
            print("Evaluating model...")
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {accuracy:.4f}")
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))
        
        if self.training_config.save_model:
            print(f"Saving model to {self.training_config.model_path}")
            joblib.dump(self.model, self.training_config.model_path)

def create_ml_trainer(data: dict, model: dict, training: dict):
    return MLTrainer(
        data=DataConfig(**data),
        model=ModelConfig(**model),
        training=TrainingConfig(**training)
    )
```

### Configuration

```yaml
# config/program/ml_training.yaml
# @package _global_
defaults:
  - base_config

_target_: ml_trainer.create_ml_trainer

data:
  train_file: "${path.data_dir}/train.csv"
  target_column: "label"
  test_size: 0.2
  random_state: 42

model:
  model_type: "random_forest"
  model_params:
    n_estimators: 100
    max_depth: 10
    random_state: 42

training:
  save_model: true
  model_path: "${path.output_dir}/model.pkl"
  evaluate: true
```

### Different Model Configurations

```yaml
# config/model/random_forest.yaml
model_type: "random_forest"
model_params:
  n_estimators: 100
  max_depth: 10
  random_state: 42
```

```yaml
# config/model/logistic_regression.yaml
model_type: "logistic_regression"
model_params:
  max_iter: 1000
  random_state: 42
  C: 1.0
```

### Usage

```bash
# Train with random forest
hprun program=ml_training

# Train with logistic regression
hprun program=ml_training model=logistic_regression

# Hyperparameter sweep
hprun -m program=ml_training model.model_params.n_estimators=50,100,200
```

## Example 3: Web Scraping with Configuration

This example shows how to build a configurable web scraping pipeline.

### Program Code

```python
# web_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse

@dataclass
class ScrapingConfig:
    base_url: str
    pages: List[str]
    delay: float = 1.0
    timeout: int = 30
    headers: Optional[Dict[str, str]] = None

@dataclass
class ExtractionConfig:
    title_selector: str
    content_selector: str
    link_selector: Optional[str] = None
    date_selector: Optional[str] = None

@dataclass
class OutputConfig:
    format: str = "csv"  # csv, json, xlsx
    filename: str = "scraped_data"
    output_dir: str = "./output"

class WebScraper:
    def __init__(self, scraping: ScrapingConfig, extraction: ExtractionConfig, output: OutputConfig):
        self.scraping_config = scraping
        self.extraction_config = extraction
        self.output_config = output
        self.session = requests.Session()
        
        if self.scraping_config.headers:
            self.session.headers.update(self.scraping_config.headers)
    
    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape a single page and extract data."""
        print(f"Scraping: {url}")
        
        try:
            response = self.session.get(url, timeout=self.scraping_config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract titles
            titles = soup.select(self.extraction_config.title_selector)
            
            # Extract content
            contents = soup.select(self.extraction_config.content_selector)
            
            # Extract links if specified
            links = []
            if self.extraction_config.link_selector:
                link_elements = soup.select(self.extraction_config.link_selector)
                links = [urljoin(url, link.get('href', '')) for link in link_elements]
            
            # Extract dates if specified
            dates = []
            if self.extraction_config.date_selector:
                date_elements = soup.select(self.extraction_config.date_selector)
                dates = [date.get_text().strip() for date in date_elements]
            
            # Combine data
            data = []
            for i, title in enumerate(titles):
                item = {
                    'title': title.get_text().strip(),
                    'content': contents[i].get_text().strip() if i < len(contents) else '',
                    'source_url': url
                }
                
                if links and i < len(links):
                    item['link'] = links[i]
                
                if dates and i < len(dates):
                    item['date'] = dates[i]
                
                data.append(item)
            
            return data
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
    
    def save_data(self, data: List[Dict]):
        """Save scraped data in the specified format."""
        from pathlib import Path
        
        output_dir = Path(self.output_config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(data)
        
        if self.output_config.format == "csv":
            filepath = output_dir / f"{self.output_config.filename}.csv"
            df.to_csv(filepath, index=False)
        elif self.output_config.format == "json":
            filepath = output_dir / f"{self.output_config.filename}.json"
            df.to_json(filepath, orient='records', indent=2)
        elif self.output_config.format == "xlsx":
            filepath = output_dir / f"{self.output_config.filename}.xlsx"
            df.to_excel(filepath, index=False)
        
        print(f"Saved {len(data)} items to {filepath}")
    
    def run(self):
        """Run the scraping pipeline."""
        all_data = []
        
        for page in self.scraping_config.pages:
            url = urljoin(self.scraping_config.base_url, page)
            page_data = self.scrape_page(url)
            all_data.extend(page_data)
            
            # Respectful delay
            time.sleep(self.scraping_config.delay)
        
        if all_data:
            self.save_data(all_data)
            print(f"Scraping completed. Total items: {len(all_data)}")
        else:
            print("No data scraped.")

def create_web_scraper(scraping: dict, extraction: dict, output: dict):
    return WebScraper(
        scraping=ScrapingConfig(**scraping),
        extraction=ExtractionConfig(**extraction),
        output=OutputConfig(**output)
    )
```

### Configuration

```yaml
# config/program/news_scraper.yaml
# @package _global_
defaults:
  - base_config

_target_: web_scraper.create_web_scraper

scraping:
  base_url: "https://example-news-site.com"
  pages:
    - "/latest"
    - "/technology"
    - "/science"
  delay: 2.0
  timeout: 30
  headers:
    User-Agent: "Mozilla/5.0 (compatible; NewsBot/1.0)"

extraction:
  title_selector: "h2.article-title"
  content_selector: "p.article-summary"
  link_selector: "h2.article-title a"
  date_selector: "time.article-date"

output:
  format: "csv"
  filename: "news_articles"
  output_dir: "${path.output_dir}/scraped"
```

### Usage

```bash
# Run the scraper
hprun program=news_scraper

# Change output format
hprun program=news_scraper output.format=json

# Adjust scraping parameters
hprun program=news_scraper scraping.delay=0.5 scraping.timeout=60
```

## Example 4: Multi-Environment Configuration

This example shows how to manage configurations across different environments.

### Environment-Specific Configurations

```yaml
# config/env/development.yaml
debug: true
log_level: "DEBUG"
database:
  host: "localhost"
  port: 5432
  name: "dev_db"
api:
  base_url: "http://localhost:8000"
  timeout: 10
```

```yaml
# config/env/staging.yaml
debug: false
log_level: "INFO"
database:
  host: "staging-db.company.com"
  port: 5432
  name: "staging_db"
api:
  base_url: "https://staging-api.company.com"
  timeout: 30
```

```yaml
# config/env/production.yaml
debug: false
log_level: "WARNING"
database:
  host: "${oc.env:DB_HOST}"
  port: "${oc.env:DB_PORT,5432}"
  name: "${oc.env:DB_NAME}"
  username: "${oc.env:DB_USERNAME}"
  password: "${oc.env:DB_PASSWORD}"
api:
  base_url: "${oc.env:API_BASE_URL}"
  timeout: 60
```

### Main Configuration

```yaml
# config/hprun.yaml
defaults:
  - hydra: default
  - path: default
  - env: development  # Default to development
  - program: my_app

# Environment can be overridden via command line
```

### Usage

```bash
# Run in development (default)
hprun

# Run in staging
hprun env=staging

# Run in production
hprun env=production

# Override specific values
hprun env=production debug=true
```

These examples demonstrate the flexibility and power of Hydra-Program's configuration system. You can adapt these patterns to your specific use cases and build sophisticated, configurable applications.
