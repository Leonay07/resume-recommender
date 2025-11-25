"""
Skills Dictionary Module

This module contains a comprehensive skill dictionary for resume parsing and job matching.
The dictionary includes technical skills, programming languages, frameworks, tools, and platforms.

Author: Renke Deng (Member A)
Shared with: Member C (for job scoring)
Version: 1.0
"""

from typing import List, Dict

# ========================================
# Main Skills Dictionary
# ========================================

SKILL_DICT = {
    # Programming Languages
    'programming_languages': [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C',
        'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala',
        'R', 'MATLAB', 'Julia', 'SQL', 'HTML', 'CSS', 'Shell',
        'Bash', 'PowerShell', 'Perl', 'Objective-C', 'Dart', 'Elixir',
        'Haskell', 'Clojure', 'F#', 'VBA', 'Groovy', 'Lua'
    ],

    # Machine Learning & Data Science Frameworks
    'ml_frameworks': [
        'TensorFlow', 'PyTorch', 'Keras', 'scikit-learn', 'XGBoost',
        'LightGBM', 'CatBoost', 'Hugging Face', 'Transformers',
        'OpenCV', 'NLTK', 'spaCy', 'Gensim', 'FastAI', 'MXNet',
        'Caffe', 'Theano', 'JAX', 'PaddlePaddle', 'ONNX',
        'MLflow', 'Weights & Biases', 'Neptune', 'Comet'
    ],

    # Data Processing & Analysis Tools
    'data_tools': [
        'Pandas', 'NumPy', 'Spark', 'Hadoop', 'Hive', 'Kafka',
        'Airflow', 'Tableau', 'Power BI', 'Excel', 'Jupyter',
        'Databricks', 'Snowflake', 'Dask', 'Polars', 'Prefect',
        'Luigi', 'Apache Beam', 'Flink', 'Storm', 'SAS',
        'SPSS', 'Looker', 'Qlik', 'Alteryx', 'Talend'
    ],

    # Cloud Platforms & Services
    'cloud_platforms': [
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'Heroku',
        'DigitalOcean', 'Alibaba Cloud', 'IBM Cloud', 'Oracle Cloud',
        'Salesforce', 'CloudFlare', 'Vercel', 'Netlify',
        'AWS Lambda', 'AWS S3', 'AWS EC2', 'AWS RDS', 'AWS EMR',
        'Azure ML', 'Google BigQuery', 'Redshift', 'Athena'
    ],

    # Databases & Data Storage
    'databases': [
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra',
        'DynamoDB', 'SQLite', 'Oracle', 'SQL Server', 'Elasticsearch',
        'Neo4j', 'MariaDB', 'CouchDB', 'Firebase', 'Supabase',
        'InfluxDB', 'TimescaleDB', 'Memcached', 'RocksDB',
        'HBase', 'Couchbase', 'ArangoDB', 'RethinkDB'
    ],

    # DevOps & Infrastructure Tools
    'devops_tools': [
        'Docker', 'Kubernetes', 'Jenkins', 'Git', 'GitHub', 'GitLab',
        'CI/CD', 'Terraform', 'Ansible', 'Prometheus', 'Grafana',
        'CircleCI', 'Travis CI', 'GitHub Actions', 'ArgoCD',
        'Helm', 'Vagrant', 'Puppet', 'Chef', 'Nagios',
        'Datadog', 'New Relic', 'Splunk', 'ELK Stack', 'Istio'
    ],

    # Web Development Frameworks
    'web_frameworks': [
        'React', 'Vue', 'Angular', 'Django', 'Flask', 'FastAPI',
        'Node.js', 'Express', 'Spring', 'ASP.NET', 'Ruby on Rails',
        'Next.js', 'Svelte', 'Laravel', 'Symfony', 'Nuxt.js',
        'NestJS', 'Gatsby', 'Remix', 'SvelteKit', 'Solid.js',
        'jQuery', 'Bootstrap', 'Tailwind CSS', 'Material UI'
    ],

    # Testing & Quality Assurance
    'testing_tools': [
        'Jest', 'Pytest', 'Selenium', 'Cypress', 'JUnit',
        'Mocha', 'Chai', 'Jasmine', 'TestNG', 'Cucumber',
        'Postman', 'SoapUI', 'JMeter', 'LoadRunner',
        'unittest', 'Robot Framework', 'Playwright', 'Appium'
    ],

    # Mobile Development
    'mobile_frameworks': [
        'React Native', 'Flutter', 'Swift', 'SwiftUI', 'Kotlin',
        'Xamarin', 'Ionic', 'Cordova', 'Android Studio', 'Xcode'
    ],

    # Version Control & Collaboration
    'collaboration_tools': [
        'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN',
        'Jira', 'Confluence', 'Trello', 'Asana', 'Slack',
        'Teams', 'Notion', 'Linear'
    ],

    # General Technical Skills & Concepts
    'technical_concepts': [
        'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
        'Data Analysis', 'Statistical Modeling', 'A/B Testing',
        'ETL', 'RESTful API', 'GraphQL', 'Microservices',
        'Agile', 'Scrum', 'Kanban', 'DevOps', 'MLOps',
        'Data Visualization', 'Big Data', 'Business Intelligence',
        'Data Engineering', 'Data Warehousing', 'Data Mining',
        'Time Series Analysis', 'Recommendation Systems',
        'Natural Language Processing', 'Image Processing',
        'Reinforcement Learning', 'Transfer Learning',
        'Neural Networks', 'Convolutional Neural Networks',
        'Recurrent Neural Networks', 'Transformer Models',
        'Object-Oriented Programming', 'Functional Programming',
        'Algorithm Design', 'Data Structures', 'System Design',
        'Distributed Systems', 'Cloud Computing', 'Edge Computing',
        'API Development', 'Web Scraping', 'Data Pipelines',
        'Feature Engineering', 'Model Deployment', 'Model Monitoring',
        'Experiment Design', 'Hypothesis Testing', 'Regression Analysis',
        'Classification', 'Clustering', 'Dimensionality Reduction',
        'Ensemble Methods', 'Gradient Boosting', 'Random Forest',
        'Support Vector Machines', 'Decision Trees', 'K-Means',
        'Principal Component Analysis', 'Cross Validation'
    ],

    # Additional Specialized Skills
    'specialized_skills': [
        'FAISS', 'Pinecone', 'Weaviate', 'ChromaDB', 'LangChain',
        'LlamaIndex', 'RAG', 'Vector Search', 'Embeddings',
        'BERT', 'GPT', 'T5', 'LLaMA', 'Claude', 'Llama',
        'Stable Diffusion', 'DALL-E', 'Whisper', 'SAM',
        'Segment Anything', 'YOLO', 'ResNet', 'VGG',
        'Blockchain', 'Smart Contracts', 'Web3', 'Solidity',
        'Cryptography', 'Cybersecurity', 'Penetration Testing',
        'Network Security', 'Information Security'
    ]
}

# ========================================
# Skill Aliases & Synonyms
# ========================================

SKILL_ALIASES = {
    # Programming Languages
    'js': 'JavaScript',
    'ts': 'TypeScript',
    'py': 'Python',
    'cpp': 'C++',
    'c++': 'C++',
    'csharp': 'C#',
    'c#': 'C#',
    'golang': 'Go',
    'node': 'Node.js',
    'nodejs': 'Node.js',

    # ML Frameworks
    'tf': 'TensorFlow',
    'tensorflow': 'TensorFlow',
    'torch': 'PyTorch',
    'pytorch': 'PyTorch',
    'sklearn': 'scikit-learn',
    'scikit': 'scikit-learn',
    'hf': 'Hugging Face',
    'huggingface': 'Hugging Face',

    # Cloud Platforms
    'aws': 'AWS',
    'amazon web services': 'AWS',
    'gcp': 'GCP',
    'google cloud platform': 'GCP',
    'azure': 'Azure',
    'microsoft azure': 'Azure',

    # Concepts
    'ml': 'Machine Learning',
    'machine learning': 'Machine Learning',
    'dl': 'Deep Learning',
    'deep learning': 'Deep Learning',
    'cv': 'Computer Vision',
    'computer vision': 'Computer Vision',
    'nlp': 'NLP',
    'natural language processing': 'NLP',
    'ai': 'Machine Learning',
    'artificial intelligence': 'Machine Learning',

    # Databases
    'postgres': 'PostgreSQL',
    'postgresql': 'PostgreSQL',
    'mongo': 'MongoDB',
    'mongodb': 'MongoDB',
    'mysql': 'MySQL',

    # DevOps
    'k8s': 'Kubernetes',
    'kubernetes': 'Kubernetes',
    'cicd': 'CI/CD',
    'ci/cd': 'CI/CD',

    # Other
    'api': 'RESTful API',
    'rest api': 'RESTful API',
    'restful': 'RESTful API',
    'bi': 'Business Intelligence',
    'business intelligence': 'Business Intelligence',
    'etl': 'ETL',
    'cnn': 'Convolutional Neural Networks',
    'rnn': 'Recurrent Neural Networks',
    'oop': 'Object-Oriented Programming',
    'fp': 'Functional Programming',
    'pca': 'Principal Component Analysis',
    'svm': 'Support Vector Machines',
    'rf': 'Random Forest',
    'gb': 'Gradient Boosting',
    'xgb': 'XGBoost',
    'lgbm': 'LightGBM'
}

# ========================================
# Helper Functions
# ========================================

def get_all_skills() -> List[str]:
    """
    Get a flattened list of all skills from the dictionary.

    Returns:
        List of all skill names

    Example:
        >>> skills = get_all_skills()
        >>> print(len(skills))
        300+
    """
    all_skills = []
    for category_skills in SKILL_DICT.values():
        all_skills.extend(category_skills)
    return all_skills


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill name to its standard form.

    This function handles:
    - Case-insensitive matching
    - Common abbreviations and aliases
    - Standardization to canonical names

    Args:
        skill: Skill name to normalize

    Returns:
        Standardized skill name

    Examples:
        >>> normalize_skill('js')
        'JavaScript'
        >>> normalize_skill('PYTHON')
        'Python'
        >>> normalize_skill('k8s')
        'Kubernetes'
    """
    skill = skill.strip()
    skill_lower = skill.lower()

    # Check for aliases first
    if skill_lower in SKILL_ALIASES:
        return SKILL_ALIASES[skill_lower]

    # Check if it matches any skill in the dictionary (case-insensitive)
    for category_skills in SKILL_DICT.values():
        for standard_skill in category_skills:
            if skill_lower == standard_skill.lower():
                return standard_skill

    # If not found, return the original skill with proper capitalization
    return skill.title()


def get_skills_by_category(category: str) -> List[str]:
    """
    Get all skills from a specific category.

    Args:
        category: Category name (e.g., 'programming_languages', 'ml_frameworks')

    Returns:
        List of skills in that category, or empty list if category not found

    Examples:
        >>> langs = get_skills_by_category('programming_languages')
        >>> print('Python' in langs)
        True
    """
    return SKILL_DICT.get(category, [])


def get_all_categories() -> List[str]:
    """
    Get all available skill categories.

    Returns:
        List of category names

    Example:
        >>> categories = get_all_categories()
        >>> print('programming_languages' in categories)
        True
    """
    return list(SKILL_DICT.keys())


def search_skills(query: str, case_sensitive: bool = False) -> List[str]:
    """
    Search for skills containing a query string.

    Args:
        query: Search query
        case_sensitive: Whether to perform case-sensitive search

    Returns:
        List of matching skills

    Examples:
        >>> results = search_skills('python')
        >>> print('Python' in results)
        True
    """
    all_skills = get_all_skills()

    if case_sensitive:
        return [skill for skill in all_skills if query in skill]
    else:
        query_lower = query.lower()
        return [skill for skill in all_skills if query_lower in skill.lower()]


def get_skill_count() -> int:
    """
    Get the total number of unique skills in the dictionary.

    Returns:
        Total number of skills

    Example:
        >>> count = get_skill_count()
        >>> print(count > 200)
        True
    """
    return len(get_all_skills())


def is_valid_skill(skill: str) -> bool:
    """
    Check if a skill exists in the dictionary.

    Args:
        skill: Skill name to check

    Returns:
        True if skill exists, False otherwise

    Examples:
        >>> is_valid_skill('Python')
        True
        >>> is_valid_skill('NotASkill123')
        False
    """
    skill_lower = skill.lower()

    # Check aliases
    if skill_lower in SKILL_ALIASES:
        return True

    # Check main dictionary
    all_skills_lower = [s.lower() for s in get_all_skills()]
    return skill_lower in all_skills_lower


# ========================================
# Module Metadata
# ========================================

__version__ = "1.0.0"
__author__ = "Renke Deng (Member A)"
__description__ = "Comprehensive skill dictionary for resume parsing and job matching"


# ========================================
# Test & Demo Code
# ========================================

if __name__ == "__main__":
    print("=" * 60)
    print("Skills Dictionary Module - Test & Demo")
    print("=" * 60)

    # Test 1: Total skill count
    print(f"\n1. Total number of skills: {get_skill_count()}")

    # Test 2: Categories
    print(f"\n2. Skill categories ({len(get_all_categories())} total):")
    for i, category in enumerate(get_all_categories(), 1):
        count = len(get_skills_by_category(category))
        print(f"   {i}. {category}: {count} skills")

    # Test 3: Skill normalization
    print("\n3. Skill normalization examples:")
    test_skills = ['js', 'PYTHON', 'k8s', 'ml', 'postgres', 'react']
    for skill in test_skills:
        normalized = normalize_skill(skill)
        print(f"   '{skill}' → '{normalized}'")

    # Test 4: Search functionality
    print("\n4. Search for 'Python' related skills:")
    results = search_skills('Python')
    print(f"   Found {len(results)} matches: {results}")

    # Test 5: Category-specific skills
    print("\n5. Sample skills from 'ml_frameworks':")
    ml_skills = get_skills_by_category('ml_frameworks')
    print(f"   {ml_skills[:10]}...")

    # Test 6: Validation
    print("\n6. Skill validation:")
    test_validations = [
        ('Python', is_valid_skill('Python')),
        ('JavaScript', is_valid_skill('JavaScript')),
        ('FakeSkill123', is_valid_skill('FakeSkill123'))
    ]
    for skill, is_valid in test_validations:
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"   {status}: {skill}")

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)
