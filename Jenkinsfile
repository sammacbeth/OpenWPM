#!/bin/env groovy

@Library('cliqz-shared-library@v1.2') _

properties([
    parameters([
        string(name: 'SITES_LIMIT', defaultValue: '500'),
    ]),
])

node('docker && gpu') {
    stage('checkout') {
        checkout scm
    }

    def dockerImage

    stage('docker build') {
        dockerImage = docker.build("cliqz-oss/openwpm:${env.BUILD_TAG}");
    }

    def HOST = helpers.getIp()
    def VNC_PORT = helpers.getFreePort(lower: 20000, upper: 20999)
    def dockerParams = "-p ${VNC_PORT}:5900 --cpus=2 --device /dev/nvidia0 --device /dev/nvidiactl"

    currentBuild.description = "VNC ${HOST}:${VNC_PORT} SITES_LIMIT: ${params.SITES_LIMIT}"
    print currentBuild.description

    dockerImage.inside(dockerParams) {
        stage('run crawl') {
            sh "/home/openwpm/OpenWPM/run_docker.sh ${params.SITES_LIMIT}"
        }

        stage('upload data') {
            withCredentials([[
              $class: 'UsernamePasswordMultiBinding',
              credentialsId: '81657070-8a22-4dc7-a24f-1856678d7722',
              passwordVariable: 'AWS_SECRET_ACCESS_KEY',
              usernameVariable: 'AWS_ACCESS_KEY_ID']]) {
                def s3Path = 's3://cliqz-mapreduce/anti-tracking/measurement_crawls/'
                sh "aws s3 cp /home/openwpm/crawl-data.sqlite ${s3Path}/crawl_${env.BUILD_NUMBER}.sqlite"
            }
        }
    }
}
