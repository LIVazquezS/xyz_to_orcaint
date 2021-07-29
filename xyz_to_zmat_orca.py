#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 19:08:50 2021

@author: vazquez
"""


from openbabel import pybel
import os

def gen_interm_zmat(infile,outfile):
    mol = next(pybel.readfile("xyz", infile)) 
    mol.write("fh",outfile)

def read_zmat(file):
    with open(file) as f:
        contents = f.read().splitlines()
        natom = int(contents[1])
        l1 = contents[2].split()
        l2 = contents[3].split()
        l3 = contents[4].split()
        rs = [0.0,l2[2],l3[2]]
        angles = [0.0,0.0,l3[4]]
        labels = [l1[0],l2[0],l3[0]]
        dhs = [0.0,0.0,0.0,0.0]
        a1_index = [0,l2[1],l3[1]]
        a2_index = [0,0,l3[3]]
        a3_index = [0,0,0,0]
        for i in range(0,natom-3):
            label, a1, r, a2, a, a3, dh = contents[5+i].split()
            labels.append(label)
            angles.append(a)
            rs.append(r)
            dhs.append(dh)
            a1_index.append(a1)
            a2_index.append(a2)
            a3_index.append(a3)
    return natom,labels,rs,angles,dhs,a1_index,a2_index,a3_index

def gen_orca_mat(natom,labels,rs,angles,dhs,a1_index,a2_index,a3_index,name):
    name = str(name) + '.zmat'
    block = []
    for k in range(0,natom):
        block.append('{:3s} {} {} {} {:15.10f} {:15.10f} {:15.10f}'.format(labels[k],a1_index[k],a2_index[k],a3_index[k],float(rs[k]),float(angles[k]),float(dhs[k])))
    with open(name, 'w', newline='') as file:
         for item in block:
             file.write("%s\n" % item)

def main(infile,ofile):
    
    gen_interm_zmat(infile,'tmp.zmat')
    natom,labels,rs,angles,dhs,a1_index,a2_index,a3_index = read_zmat('tmp.zmat')
    gen_orca_mat(natom,labels,rs,angles,dhs,a1_index,a2_index,a3_index,ofile)
    os.remove('tmp.zmat')
    print('Conversion Done, Be happy')
    
    
main('1a.xyz','orca')