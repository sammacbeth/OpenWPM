#!/bin/env groovy

node('docker && gpu') {
    stage('checkout') {
        checkout scm
    }

    def dockerImage

    stage('docker build') {
        dockerImage = docker.build("cliqz-oss/openwpm:${env.BUILD_TAG}");
    }

    dockerImage.inside() {
        stage('run crawl') {
            sh '/home/openwpm/OpenWPM/run_docker.sh'
        }

        stage('upload data') {
            withCredentials([[
              $class: 'UsernamePasswordMultiBinding',
              credentialsId: '',
              passwordVariable: 'AWS_SECRET_ACCESS_KEY',
              usernameVariable: 'AWS_ACCESS_KEY_ID']]) {
                def s3Path = 's3://cliqz-mapreduce/anti-tracking/measurement_crawls/'
                sh "aws s3 cp /home/openwpm/crawl-data.sqlite ${s3Path}/crawl_${env.BUILD_NUMBER}.sqlite"
            }
        }
    }
}
