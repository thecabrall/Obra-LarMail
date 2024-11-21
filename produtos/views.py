from django.shortcuts import render,HttpResponse
from django.template.loader import render_to_string
import csv
import os
from.form import CSVUploadForm

# Create your views here.

arquivo = [['thumb', 'nome', 'linkcompra', 'preco_anterior', 'preco_atual','img1','img2','img3','img4','img5','linkimg1','linkimg2','linkimg3','linkimg4','linkimg5']]

# email = 'email_ramada.html'
# email_ol = 'email_obraelar.html'
# email_rm = 'email_ramada.html'
# email_lc = 'email_lindacor.html'

def csv_enviado(request):
    produtos = []
    pictures = []
    try:
        if request.method == 'POST':
            email = request.POST['modelos']
            price = request.POST['prices']
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                planilha = request.FILES['arquivo_csv']
                decode = planilha.read().decode('utf-8').splitlines()
                plan_dec = csv.DictReader(decode,delimiter=";")
                for linha in plan_dec:
                    # linha = {k.strip(): v for k, v in linha.items()}
                    prod = {
                        'thumb': linha['thumb'],
                        'nome': linha['nome'],
                        'linkcompra': linha['linkcompra'],
                        'preco_anterior': linha['preco_anterior'],
                        'preco_atual': linha['preco_atual'],
                        'img1': linha['img1'],
                        'img2': linha['img2'],
                        'img3': linha['img3'],
                        'img4': linha['img4'],
                        'img5': linha['img5'],
                        'linkimg1': linha['linkimg1'],
                        'linkimg2': linha['linkimg2'],
                        'linkimg3': linha['linkimg3'],
                        'linkimg4': linha['linkimg4'],
                        'linkimg5': linha['linkimg5'],
                    }

                    produtos.append(prod)
                    pictures.append(prod)
                request.session['produtos'] = produtos[:8]
                request.session['modelos'] = email
                request.session['prices'] = price
                produtos = request.session['produtos']
                banners_lista = pictures[0:1:1]
                banner = banners_lista[0]
                request.session['pictures'] = banner
                return render(request, f'produtos/{email}', {'produtos': produtos,'banner':banner, 'price':price},print(price))
        else:
            form = CSVUploadForm()
        return render(request, 'produtos/upload.html', {'form': form})
    except KeyError:
        return HttpResponse('<h1>Os valores de uma das colunas está incorreto.</h1><br><br><br><a href="https://obra-larmail.onrender.com"> Clique aqui para voltar </a></h1> ')
    except IndexError:
        return HttpResponse('<h1>Existe colunas Vazias ou com valores incorretos.<br><br><br><a href="https://obra-larmail.onrender.com"> Clique aqui para voltar </a></h1> ')
    except Exception as e:
        return HttpResponse(f'<h1>Ocorreu um erro desconhecido, informe o erro seguite ao criador. Erro : {e}')
    

def html_download(request):
    produtos = request.session.get('produtos')
    email = request.session.get('modelos')
    banner = request.session.get('pictures')
    price = request.session.get('prices')
    if not produtos:
        return HttpResponse("<h1>Nenhum produto disponível para download.</h1>", status=404)
    
    conteudo = render_to_string(f'produtos/{email}',{
        'produtos':produtos,
        'banner':banner,
        'price':price,
        'download':True
        },print(price))
    response = HttpResponse(conteudo,content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="email_marketing.html"'
    return response


def download_modelo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="modelo.csv"'
    leitor = csv.writer(response, delimiter=';')
    leitor.writerow(['thumb', 'nome', 'linkcompra', 'preco_anterior', 'preco_atual','img1','img2','img3','img4','img5','linkimg1','linkimg2','linkimg3','linkimg4','linkimg5'])    
    return response