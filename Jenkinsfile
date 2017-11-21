#!/bin/env groovy

@Library('cliqz-shared-library@v1.2') _

properties([
    parameters([
        string(name: 'SITES_LIMIT', defaultValue: '500'),
        string(name: 'SCREEN_RESOLUTION', defaultValue: '1234x1000x24'),
        choice(name: 'TIMEZONE', defaultValue: 'UTC', choices: 'UTC\nEurope/Berlin\nAmerica/New_York'),
        booleanParam(name: 'INSTALL_FONTS', defaultValue: false),
        booleanParam(name: 'GHOSTERY', defaultValue: false),
        string(name: 'SITES_LIST', defaultValue: './lists/sites.txt'),
        choice(name: 'AWS_REGION', defaultValue: 'us-east-1', choices: 'us-east-1\neu-central-1')
    ]),
])

node("docker && gpu && ${params.AWS_REGION}") {
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
    def crawlParams = "${params.SCREEN_RESOLUTION} ${params.SITES_LIMIT} ${params.SITES_LIST}"
    if (params.GHOSTERY) {
        crawlParams += " --ghostery"
    }

    currentBuild.description = "VNC ${HOST}:${VNC_PORT} SITES_LIMIT: ${params.SITES_LIMIT}"
    print currentBuild.description

    dockerImage.inside(dockerParams) {
        stage('configure machine') {
            // set timezone
            sh "sudo ln -sf /usr/share/zoneinfo/${params.TIMEZONE} /etc/localtime"
            // fonts
            if (params.INSTALL_FONTS) {
                sh "sudo apt install ttf-ubuntu-font-family"
            }
        }

        stage('run crawl') {
            sh "/home/openwpm/OpenWPM/run_docker.sh ${crawlParams}"
        }

        stage('upload data') {
            withCredentials([[
              $class: 'AmazonWebServicesCredentialsBinding',
              credentialsId: '81657070-8a22-4dc7-a24f-1856678d7722',
              secretKeyVariable: 'AWS_SECRET_ACCESS_KEY',
              accessKeyVariable: 'AWS_ACCESS_KEY_ID']]) {
                def s3Path = 's3://cliqz-mapreduce/anti-tracking/measurement_crawls'
                sh "aws s3 cp /home/openwpm/crawl-data.sqlite ${s3Path}/crawl_${env.BUILD_NUMBER}.sqlite"
            }
        }
    }
}
