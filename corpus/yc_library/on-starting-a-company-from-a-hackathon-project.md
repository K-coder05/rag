---
title: On starting a company from a hackathon project
source: https://www.ycombinator.com/library/4x-on-starting-a-company-from-a-hackathon-project
---

A couple years ago, [Athelas](https://athelas.com/) (YC S16) started as a proof-of-concept project built overnight at [YC Hacks 2014](https://ychacks.devpost.com/submissions/25781-athelas). This month we started shipping our first devices to patients and hospitals around the country. We learned a lot in the process and wanted to share a few thoughts here.

[![athelas-1](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-1.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-1.png)

The device is a low-cost imager that enables rapid blood diagnostics through computer vision instead of traditional lab-based techniques. Going from a hacked together hardware prototype to shippable product (especially in the medical field) was a progression in dimensionality at every stage, and it’s quite interesting now to look back at day 1.

The first version that began at the hackathon used a rubber piece and spherical magnifier attached to a smartphone camera. A blood sample would be held (by a toilet paper roll) underneath, the camera would take a couple images, then produce the computer vision rendered malaria cell counts. In design this is quite similar to a [van Leeuwenhoek microscope](https://en.wikipedia.org/wiki/Antonie_van_Leeuwenhoek) (considered one of the earliest microscopes ever built) which was used to see microorganisms for the first time in human history. There were a few examples of this setup, and I spent the first couple hours of the hackathon getting it to work consistently on my phone.

[![athelas-2](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-2.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-2.png)

[![athelas-4](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-4.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-4.png)

[![athelas-5](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-5.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-5.png)

*Above: A few excerpts from a writeup I did on Athelas a few months after the hackathon.*

The real focus of the hack was writing segmentation and template matching approaches, combined with a fast random forest model implementation that learned to classify extracted versions of the Red Blood Cells (RBCs). Cell boundaries would be recognized, then fed into the classier to identify whether a parasitical cell (like Malaria or Trypanosoma) was present.

[![athelas-6](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-6.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-6.png)

This made for a fun demo, where a sample slide would have malaria tagged in it, but a normal person’s blood would not. While functioning and a neat trick, someone needed to be physically holding the camera in place, the slide had to be moved around, with the lighting often being hard to fix. At the end of the day it was a nice experimental toy you might see someone post as a video on Facebook.

![YC Logo](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAMAAABPMuDPAAAAQlBMVEXyZSLyZSLyZSLyZSLyZSL6roH91br2ilD+6tr4nGn0eDf7wp3+9e3zbyz3k1z0gUP7uI/5pXX+38n8y6z////yZSKuMvVfAAAABXRSTlOAQMBgICelMzEAAAOgSURBVHhe5MABDQAAAIIw3eifmSB8vA3Zt5vcuGEgCsLeUBSpnxnb4f2vmn068xK5Z8FuFQ8gCB9q80Dw42Pc+3y8UQABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQACBR7GnuAF6MafNKnDsv+xx/+1mv3nOKjDKXwRWbwIWYJl4F6wigvclUCcWaCKCeRKwAtNFoBN4TC1wigjelMA2+S5YRATv+VyfXKC+NYIqEphVQEfgT2Dv0ws8VAT+BEqAXbCJCPwJHAEEuorAn0AAARGBO4H1CCFw7O+JoArIuQVGERH4EhgBBFQE/gQmF9ARnP4EljG5gB5Iiz+BGkBAreTqTyCAgIzAnUAogdMbwSIm0cQCeiAtvgR6MIEqInAkEEBARuBKIJzAwxOB5SsBb822n0dQxSoOJNBFBI4EAgmMp4jAkUAAATWQ6s8SaEFvz8vPIqhiWAYQcEQgEogqMD5FBBcS+BrBBPRAqtcTqIEF2vUIqsgmgIAjApFAaIF6NQKbwPcIKKAHUr2WQI8k4I+gilUcQMARgUggvEC/EkEzAM8E7wu2CxGsdhJFEvBH0MQqDiegV3J1JBBQ4NhFBDqBzyTvC4qIQCawjgwCOgKdQIstoFdydSQQRcD2rSNoVimRQPuPCFaLFF1AR7A5EggloK/BdAIZBPRVqE6ghxLwR7BaoBQCOgKdQDqBLiIQCSQSGJuIoNlJlEVAR3C8TKCkfHX7fLn+T5tASoFjf9X6YmlSCozyYvxVO4kSCegI1r8n0FIJ6IF0igQyCej9txiWZAI6gsfoViWxwPiy+2gzqzi1QLUR2ATSCeiBtBuSfAI6AjsWkguM738I9PQC3ZFADoGxKYC95xfQEZRxA4FRRALHLQSOXSSQXkBHsB75BXQEbWQV0APJruL8AmMVCaQW0BEsI5uAXsn21FsJVJFAZgH9juJmAsVOorsLlLsJIIAAAggggAACCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAggggAACCCCAAAIIIIAAAm3547QAAoGPFkAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBBBAAAEEEEAAAQQQQAABBH6XAwc0AAAAAME2+ncWxOXNAI6Cs14i3Db7AAAAAElFTkSuQmCC)

# What is Y Combinator?

We're an accelerator that funds startups — like Coinbase, Instacart, Reddit, Doordash — at their earliest stages. Starting a company? Even if it feels early, 40% of our companies joined with just an idea.

[Apply](/apply)

But we were sure it could be more. The core idea was - if we made it broad-ranging and easy enough for anyone to use - why not have a simple blood screen in every doctor’s office, nursing facility, or even home? After heading back to school, this idea consumed us and we decided to continue it - but as a product - not just a demo. That meant creating an automated blood processing mechanism to generate a stained peripheral smear, a more robust computer vision approach for different cell types, automated mechanisms to image the whole sample without holding the slide in place, and most importantly - clinical validation.

Deepika (my cofounder) worked to perfect the fast staining mechanism and come up with a way to coat them on plastic strips that could be ready to use out of the box. She worked mostly in-lab, synthesizing dozens of versions of the stain compound, and observing empirically the quality of cell rendering. The other side of this problem was ensuring that the strip could easily be compressed to create a ‘monolayer’, or single layer of cells that enables statistically representative imaging.

[![athelas-7](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-7.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-7.png)

[![athelas-8](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-8.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-8.png)

*Above: An excerpt from “The marching velocity of the capillary meniscus in a microchannel”, a sample of work we referenced when attempting to model the flow in our channel to generate a monolayer. This capillary design was eventually shelved for a future iteration.*

In the meantime, I focused on building a higher resolution optical set up in a still cheap, but stand-alone device. As such, we could focus on monitoring more prevalent cell-types like Leukocytes and Platelets (beyond just malaria). The heart of it was an actuation system, coupled with gaussian edge autofocusing algorithms to ensure that our cells were being captured in a consistent fashion. Here’s a prototype midway through:

[![athelas-9](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-9.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-9.png)

Furthermore, we started assembling a training set of data from public CDC images, blood smears collected from researchers at Stanford and UCSF - often hand labeled by me or a pathologist. From there, we were able to employ traditional computer vision and deep learning approaches to recognize and classify cell types based on previous, human-guided examples.

[![athelas-10](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-10.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-10.png)

*Cell body extraction post hough transform, first pass, pre-segmentation and classification*

The first set of progress was slow. College workload at Stanford + rising costs of our hardware iterations often made it difficult for us to operate with the iteration speeds a normal product needs. Finals often meant days going by without any tangible progress whatsoever. But we put together a tangible, usable v1, that could grab images of a stained blood sample, and process. [See the demo here](https://www.youtube.com/watch?v=fEcx3hx-398).

Then this summer, things came full circle to that orange building in Mountain View, as we joined the summer batch at Y Combinator. Our time (now full time on the project) was focused on our clinical validation locally and at the FEMAP family hospital, to run a first set of usages within a hospital system. The goal was proving the system on just one aspect first: White Blood Cell counts. By grabbing images of samples on our strip, and then running the algorithms we showed how our counts were correlating with high accuracy to the gold standard Beckman Counter across 350 patients, combined with [a set of bench precision studies](http://athelas.com/data).

[![athelas-11](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-11.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-11.png)

An interesting aspect was showing how our drop to drop precision [(something of much recent interest)](https://www.jci.org/articles/view/86318) was clinically acceptable versus other systems operating on drops. Coulter counters (traditional cell counting systems) work by flowing particles through a jeweled aperture a few microns in diameter, and recording impedance to register particle size - and as a result, particle classification. At the crux of it, [higher impedance = larger particle size](http://www.cyto.purdue.edu/cdroms/cyto2/6/coulter/ss000103.htm).

[![athelas-12](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-12.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-12.png)

Coulter Counting Principle diagram source: [cyto.purdue.edu](http://cyto.purdue.edu)

Athelas’s computer vision approach, however, focuses wholly on the image and nucleation patterns. As such, the particulate matter or lymph that can often confuse a Coulter system (especially in diluted quantities), is simply classified by the vision as a non-leukocyte cellular body (not a white blood cell, but some other, un-classified artifact in the blood sample).

[![athelas-13](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-13.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-13.png)

The trial showed high inter-rater agreement (100% 5-class inter rater agreement) between the two systems, we submitted our data off to the FDA for Class 2 510k approval, and are now distributing our Class 1 version of the system for rapid White Blood Cell monitoring. See more at [athelas.com](http://athelas.com).

[![athelas-14](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-14.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-14.png)

[![athelas-15](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-15.png)](https://blog.ycombinator.com/wp-content/uploads/2017/01/athelas-15.png)

As we integrate new blood tests into the system over the coming months (concussion monitoring, inflammation tracking, urinary tract infection, platelets, more cell counts), our key growing challenge will be working with the existing clinical and medical community to help guide adoption and usage. These coming months will focus on getting our $250 devices into as many point-of-care locations, homes, and clinical settings as possible.

We’re always looking for awesome people to meet and hackers to join our growing team, so shoot me an email if you want to chat about anything: tanay [at] [getathelas.com](http://getathelas.com)