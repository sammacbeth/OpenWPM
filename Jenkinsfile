#!/bin/env groovy

node('docker && gpu') {
  stage('checkout') {
    checkout scm
  }

  def imgName = "cliqz-oss/openwpm:${env.BUILD_TAG}"

  stage('docker build') {
    sh "docker build -t ${imgName} ."
  }

  docker.image(imgName).inside() {
    stage('run crawl') {
      sh '/home/openwpm/OpenWPM/run_docker.sh'
    }

    stage('upload docs') {
      withCredentials([[
        $class: 'UsernamePasswordMultiBinding',
        credentialsId: '',
        passwordVariable: 'AWS_SECRET_ACCESS_KEY',
        usernameVariable: 'AWS_ACCESS_KEY_ID']]) {

        def s3DocPath = 's3://cliqz-mapreduce/anti-tracking/measurement_crawls/'

        sh "aws s3 cp /home/openwpm/crawl-data.sqlite ${s3DocPath}/crawl_${env.BUILD_NUMBER}.sqlite"
      }
    }
  }
}

