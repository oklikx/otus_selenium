pipeline {
    agent any

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://selenoid.example.com:4444/wd/hub', description: 'Адрес Selenoid (executor)')
        string(name: 'APP_URL', defaultValue: 'http://prestashop.example.com', description: 'Адрес приложения PrestaShop')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: 'latest', description: 'Версия браузера')
        string(name: 'THREADS', defaultValue: '2', description: 'Количество потоков')
    }

    environment {
        SELENOID_URL    = "${params.SELENOID_URL}"
        APP_URL         = "${params.APP_URL}"
        BROWSER         = "${params.BROWSER}"
        BROWSER_VERSION = "${params.BROWSER_VERSION}"
        THREADS         = "${params.THREADS}"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/oklikx/otus_selenium.git', branch: 'homework_28.09.26'
            }
        }

        stage('Prepare venv') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    . .venv/bin/activate
                    pytest \
                        --clean-alluredir \
                        -n "$THREADS" \
                        --selenoid-url="$SELENOID_URL" \
                        --url="$APP_URL" \
                        --browser="$BROWSER" \
                        --browser-version="$BROWSER_VERSION"
                """
            }
        }
    }

    post {
        always {
            allure([
                commandline: 'allure',
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
    }
}