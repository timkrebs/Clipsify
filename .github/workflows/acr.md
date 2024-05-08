name: ACR CI

on: [push]

jobs:
  build-auth:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout GitHub Action'
        uses: actions/checkout@main
        
      - name: 'Login via Azure CLI'
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: 'Build and push auth image'
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      - run: |
          cd app/auth/
          docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/auth:${{ github.sha }}
          docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/auth:${{ github.sha }}

      - name: 'Deploy auth to Azure Container Instances'
        uses: azure/aci-deploy@v1
        with:
          resource-group: ${{ secrets.RESOURCE_GROUP }}
          dns-name-label: ${{ secrets.RESOURCE_GROUP }}-auth-${{ github.run_number }}
          image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/auth:${{ github.sha }}
          registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          registry-username: ${{ secrets.REGISTRY_USERNAME }}
          registry-password: ${{ secrets.REGISTRY_PASSWORD }}
          name: aci-auth
          location: 'west us'

  build-gateway:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout GitHub Action'
        uses: actions/checkout@main
        
      - name: 'Login via Azure CLI'
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: 'Build and push gateway image'
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      - run: |
          cd app/gateway/
          docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/gateway:${{ github.sha }}
          docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/gateway:${{ github.sha }}

      - name: 'Deploy gateway to Azure Container Instances'
        uses: azure/aci-deploy@v1
        with:
          resource-group: ${{ secrets.RESOURCE_GROUP }}
          dns-name-label: ${{ secrets.RESOURCE_GROUP }}-gateway-${{ github.run_number }}
          image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/gateway:${{ github.sha }}
          registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          registry-username: ${{ secrets.REGISTRY_USERNAME }}
          registry-password: ${{ secrets.REGISTRY_PASSWORD }}
          name: aci-gateway
          location: 'west us'
    
  build-converter:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout GitHub Action'
        uses: actions/checkout@main
        
      - name: 'Login via Azure CLI'
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: 'Build and push converter image'
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      - run: |
          cd app/converter/
          docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/converter:${{ github.sha }}
          docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/converter:${{ github.sha }}

      - name: 'Deploy converter to Azure Container Instances'
        uses: azure/aci-deploy@v1
        with:
          resource-group: ${{ secrets.RESOURCE_GROUP }}
          dns-name-label: ${{ secrets.RESOURCE_GROUP }}-converter-${{ github.run_number }}
          image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/converter:${{ github.sha }}
          registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          registry-username: ${{ secrets.REGISTRY_USERNAME }}
          registry-password: ${{ secrets.REGISTRY_PASSWORD }}
          name: aci-converter
          location: 'west us'

  build-notification:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout GitHub Action'
        uses: actions/checkout@main
        
      - name: 'Login via Azure CLI'
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: 'Build and push notification image'
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      - run: |
          cd app/notification/
          docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/notification:${{ github.sha }}
          docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/notification:${{ github.sha }}

      - name: 'Deploy notification to Azure Container Instances'
        uses: azure/aci-deploy@v1
        with:
          resource-group: ${{ secrets.RESOURCE_GROUP }}
          dns-name-label: ${{ secrets.RESOURCE_GROUP }}-notification-${{ github.run_number }}
          image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/notification:${{ github.sha }}
          registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          registry-username: ${{ secrets.REGISTRY_USERNAME }}
          registry-password: ${{ secrets.REGISTRY_PASSWORD }}
          name: aci-notification
          location: 'west us'
