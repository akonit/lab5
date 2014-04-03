from django.views import generic
from products.models import Product, Opinion, Category
from products.forms import OpinionForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

class IndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'product_list'
    encoding = 'utf8'

    def get_queryset(self):
        return Product.objects.all()

class DetailView(generic.DetailView):
    model = Product
    template_name = 'products/detail.html'
    encoding = 'utf8'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        product = kwargs['object']
        category_names = []
        for category in product.categories:
            c = Category.objects.get(id=category)
            category_names.append(c.name)
        context['category_names'] = category_names
        context['form'] = OpinionForm
        flatten_opinions = []
        for opinion in product.opinions:
            old_opinion = Opinion.create()
            old_opinion.login = opinion[1]["login"]
            old_opinion.text = opinion[1]["text"]
            old_opinion.pub_date = opinion[1]["pub_date"]
            flatten_opinions.append(old_opinion)
        context['flatten_opinions'] = flatten_opinions
        return context

def addOpinion(request, pk):
    request.encoding = 'utf8'
    p = request.POST

    if p.has_key("text") and p["text"]:
        product = Product.objects.get(id=pk)
        new_opinion = Opinion.create()
        new_opinion.login = "Anonim"
        if p.has_key("login") and p["login"]:
            new_opinion.login = p["login"]
        new_opinion.text = p["text"]
        new_opinion.pub_date = datetime.now()
        opinions = []
        for opinion in product.opinions:
            old_opinion = Opinion.create()
            old_opinion.login = opinion[1]["login"]
            old_opinion.text = opinion[1]["text"]
            old_opinion.pub_date = opinion[1]["pub_date"]
            opinions.append(old_opinion)

        opinions.append(new_opinion)
        product.opinions = opinions
        product.save()
    return HttpResponseRedirect(reverse("products.views.post", args=[pk]))

def post(request, pk):
    request.encoding = 'utf8'
    product = Product.objects.get(pk=pk)
    opinions = Opinion.objects.filter(product=product)
    d = dict(product=product, opinions=opinions, form=OpinionForm(), user=request.user)
    d.update(csrf(request))
    return render_to_response("products/detail.html", d)

#search by product description
def filteredIndexView(request, pk):
    request.encoding = 'utf8'
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        products = Product.objects.filter(description__icontains=q)
        return render(request, 'products/index.html',
            {'product_list': products})
    else:
        products = Product.objects.all()
        return render(request, 'products/index.html',
            {'product_list': products})

@csrf_exempt
def vote(request, pk):
    request.encoding = 'utf8'
    p = request.POST
    product = Product.objects.get(id=pk)
    mark = p.get('mark', False)
    product.mark = (product.mark * product.voters + int(mark)) / (product.voters + 1);
    product.voters = product.voters + 1;


    flatten_opinions = []
    for opinion in product.opinions:
        old_opinion = Opinion.create()
        old_opinion.login = opinion[1]["login"]
        old_opinion.text = opinion[1]["text"]
        old_opinion.pub_date = opinion[1]["pub_date"]
        flatten_opinions.append(old_opinion)

    product.opinions = flatten_opinions
    product.save();

    return render_to_response("products/detail.html", {'product': product})